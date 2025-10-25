#!/usr/bin/env python3
"""
Scraper robusto para https://www.fundsexplorer.com.br/ranking
- Intercepta respostas de rede (XHR/Fetch) via Playwright e tenta extrair JSON com os dados.
- Fallback: extrai a tabela do DOM após rolagem e espera.
- Normaliza nomes para ASCII, renomeia 'papel'/'fundos' -> 'ticker', tenta converter números.
- NÃO salva em Excel; mostra o DataFrame no final.
"""

import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import pandas as pd
import unicodedata, re, math, time

URL = "https://www.fundsexplorer.com.br/ranking"
NAV_TIMEOUT_MS = 20000

# utilitários
def ascii_colname(s: str) -> str:
    if s is None:
        return s
    s = str(s).strip()
    s = unicodedata.normalize("NFKD", s)
    s = s.encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^\w\s\-\%\/\(\)\.,:$]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s.upper()  # deixo em maiúsculas para visualização consistente

def try_parse_number_like(s):
    if s is None:
        return s
    if isinstance(s, (int, float)):
        return float(s)
    s = str(s).strip()
    if s == "":
        return s
    s2 = s.replace("R$", "").replace("%", "").replace(".", "").replace("\xa0", "").strip()
    # tentar detectar vírgula decimal
    if "," in s2 and s2.count(",") == 1:
        s2 = s2.replace(",", ".")
    # remover espaços e sinais extras
    s2 = re.sub(r"[^\d\-\.\+eE]", "", s2)
    if s2 in ("", ".", "-", "+"):
        return s
    try:
        v = float(s2)
        return v
    except Exception:
        return s

# detecta se um objeto é plausível como "lista de registros de tabela"
def is_plausible_table_list(obj):
    if not isinstance(obj, list):
        return False
    if len(obj) == 0:
        return False
    # verificar se elementos são dicts com múltiplas keys
    sample = obj[0]
    return isinstance(sample, dict) and len(sample.keys()) >= 2

async def fetch_page_and_capture_json(url=URL, headless=True, timeout_ms=NAV_TIMEOUT_MS):
    candidates = []  # lista de (url, parsed_json)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        page = await browser.new_page()
        # coletar respostas
        responses = []

        def on_response(response):
            # coletar apenas respostas com content-type json ou que terminem com .json
            try:
                rurl = response.url
                # armazenar response object; we'll try to json() them later
                responses.append(response)
            except Exception:
                pass

        page.on("response", on_response)

        try:
            await page.goto(url, timeout=timeout_ms)
        except PlaywrightTimeoutError:
            await page.goto(url)

        # esperar um pouco para XHRs carregarem
        await page.wait_for_timeout(2000)
        # forçar rolagem para disparar carregamento lazy/virtualized
        await page.evaluate("""() => { window.scrollTo(0, document.body.scrollHeight); }""")
        await page.wait_for_timeout(1500)
        await page.evaluate("""() => { window.scrollTo(0, 0); }""")
        await page.wait_for_timeout(500)

        # tentar processar as respostas capturadas - pegar as que contem json
        for resp in responses:
            try:
                # filtrar por status 200
                status = resp.status
                if status != 200:
                    continue
                # tentar obter header content-type
                try:
                    headers = await resp.all_headers()
                    ct = headers.get("content-type","")
                except Exception:
                    ct = ""
                # Preferir JSONs
                if "application/json" in ct or resp.url.endswith(".json") or "api" in resp.url.lower() or "ranking" in resp.url.lower() or "funds" in resp.url.lower():
                    # tentar json
                    try:
                        j = await resp.json()
                        candidates.append((resp.url, j))
                    except Exception:
                        # some responses may not be valid json; skip
                        continue
            except Exception:
                continue

        await browser.close()
    return candidates

# fallback DOM extractor: pega tabela visível lendo innerText das células
# retorna DataFrame
def extract_table_from_grid_js_result(grid):
    # grid = list of rows (lists)
    if not grid:
        return pd.DataFrame()
    ncols = max(len(r) for r in grid)
    # determinar count header rows by heuristic
    def alpha_numeric_counts(row):
        letters = sum(1 for c in row if isinstance(c, str) and re.search(r"[A-Za-zÀ-ÿ]", c))
        digits = sum(1 for c in row if isinstance(c, str) and re.search(r"[0-9]", c))
        return letters, digits

    header_rows = 0
    for row in grid:
        a,n = alpha_numeric_counts(row)
        if a >= n:
            header_rows += 1
        else:
            break
    if header_rows == 0:
        header_rows = 1

    headers = grid[:header_rows]
    data = grid[header_rows:]

    colnames = []
    for j in range(ncols):
        parts = [h[j].strip() for h in headers if j < len(h) and isinstance(h[j], str) and h[j].strip() != ""]
        colnames.append(" - ".join(parts) if parts else f"col_{j}")

    normalized_rows = []
    for row in data:
        new = [ (row[i] if i < len(row) else "") for i in range(ncols) ]
        normalized_rows.append(new)

    df = pd.DataFrame(normalized_rows, columns=colnames)
    return df

async def dom_extract_with_playwright(url=URL, headless=True, timeout_ms=NAV_TIMEOUT_MS):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        page = await browser.new_page()
        try:
            await page.goto(url, timeout=timeout_ms)
        except PlaywrightTimeoutError:
            await page.goto(url)
        # aguardar tabela ou algumas linhas
        try:
            await page.wait_for_selector("table tbody tr, table tr", timeout=timeout_ms)
        except PlaywrightTimeoutError:
            pass
        # scroll incremental para forçar renderização de linhas
        for y in range(0, 3000, 800):
            await page.evaluate(f"() => window.scrollTo(0, {y});")
            await page.wait_for_timeout(300)
        # executar js que constrói grid (respeita colspan/rowspan)
        js_extract = """
        () => {
            function tableToGrid(table) {
                const rows = Array.from(table.querySelectorAll('tr'));
                const grid = [];
                const occupied = {};
                let maxCols = 0;
                for (let r = 0; r < rows.length; r++) {
                    if (!grid[r]) grid[r] = [];
                    const tr = rows[r];
                    const cells = Array.from(tr.querySelectorAll('th,td'));
                    let c = 0;
                    for (const cell of cells) {
                        while (occupied[`${r},${c}`]) c++;
                        const rowspan = cell.rowSpan || 1;
                        const colspan = cell.colSpan || 1;
                        const text = (cell.innerText || "").trim();
                        while (grid[r].length < c) grid[r].push('');
                        grid[r][c] = text;
                        for (let rr = r; rr < r + rowspan; rr++) {
                            for (let cc = c; cc < c + colspan; cc++) {
                                occupied[`${rr},${cc}`] = true;
                                if (!grid[rr]) grid[rr] = [];
                                while (grid[rr].length <= cc) grid[rr].push('');
                                if (!(rr === r && cc === c)) grid[rr][cc] = grid[rr][cc] || '';
                            }
                        }
                        c += colspan;
                        if (c > maxCols) maxCols = c;
                    }
                    while (grid[r].length < maxCols) grid[r].push('');
                }
                const finalMax = Math.max(...grid.map(r => r.length));
                for (let i=0;i<grid.length;i++){
                    while (grid[i].length < finalMax) grid[i].push('');
                }
                return grid;
            }
            const table = document.querySelector('table');
            if (!table) return {error:'no_table'};
            return {error:null, grid: tableToGrid(table)};
        }
        """
        result = await page.evaluate(js_extract)
        await browser.close()
    if result is None or result.get("error"):
        return pd.DataFrame()
    return extract_table_from_grid_js_result(result["grid"])

# função principal que combina estratégias
async def scrape_best():
    # 1) tentar capturar respostas JSON durante o carregamento
    candidates = await fetch_page_and_capture_json(headless=True)
    # tentar achar candidato plausível
    for url, obj in candidates:
        # Se próprio obj é lista plausível
        if is_plausible_table_list(obj):
            df = pd.DataFrame(obj)
            print("Encontrado JSON direto em:", url)
            return df
        # se dict com 'data'/'items'/'results'
        if isinstance(obj, dict):
            for k in ("data","items","results","rows","funds"):
                if k in obj and is_plausible_table_list(obj[k]):
                    print(f"Encontrado JSON em {url} -> chave '{k}'")
                    df = pd.DataFrame(obj[k])
                    return df
    # 2) fallback DOM extraction
    print("Nenhum JSON válido detectado nas respostas; executando extração via DOM (Playwright).")
    df_dom = await dom_extract_with_playwright(headless=True)
    if df_dom.empty:
        print("Extração DOM retornou DataFrame vazio.")
        return df_dom
    # normalizar colunas e converter
    df_dom.columns = [ascii_colname(c) for c in df_dom.columns]
    # rename common col names to ticker
    df_dom = df_dom.rename(columns={c:"TICKER" for c in df_dom.columns if c.lower() in ["fundos","papel"]})
    # tentar converter valores
    for col in df_dom.columns:
        df_dom[col] = df_dom[col].apply(try_parse_number_like)
    return df_dom

# executa e mostra resultado
if __name__ == "__main__":
    df = asyncio.run(scrape_best())
    print("\n=== Resultado final ===")
    print("Shape:", df.shape)
    # mostrar cabeçalho (10 linhas) no console
    if df.empty:
        print("DataFrame vazio — nenhuma estratégia encontrou os dados.")
        print("Se possível, abra seu navegador, abra DevTools > Network > XHR e recarregue a página; copie a requisição que retorna os dados da tabela (URL) e cole aqui que eu adapto um requests direto para esse endpoint.")
    else:
        # normalizar nomes finais (upper + ASCII) e imprimir
        df.columns = [ascii_colname(c) for c in df.columns]
        # renomear novamente 'papel'-> ticker se necessário
        for c in list(df.columns):
            if c.lower() in ("papel","fundos"):
                df = df.rename(columns={c:"TICKER"})
        # garantir ticker first column if exists
        cols = list(df.columns)
        if "TICKER" in cols:
            cols = ["TICKER"] + [c for c in cols if c!="TICKER"]
            df = df[cols]
        # tentar converter colunas numéricas (já feito parcialmente)
        print(df.head(10).to_string())

