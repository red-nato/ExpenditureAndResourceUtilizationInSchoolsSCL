"""Genera y ejecuta el notebook. No contiene resultados prefabricados."""
from pathlib import Path
import argparse, html, json, os, re, sys, tempfile
import nbformat
from nbclient import NotebookClient
ROOT = Path(__file__).resolve().parents[2]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-execute', action='store_true')
    args = parser.parse_args()
    source = (ROOT/'analysis/scripts/eda_notebook_source.py').read_text()
    chunks = re.split(r'^# %%([^\n]*)\n', source, flags=re.M)
    cells = []
    for kind, body in zip(chunks[1::2], chunks[2::2]):
        if '[markdown]' in kind:
            body = '\n'.join(re.sub(r'^# ?', '', line) for line in body.strip().splitlines())
            cells.append(nbformat.v4.new_markdown_cell(body))
        else:
            cells.append(nbformat.v4.new_code_cell(body.strip()))
    nb = nbformat.v4.new_notebook(cells=cells, metadata={
        'kernelspec': {'name':'python3','display_name':'Python 3','language':'python'},
        'language_info': {'name':'python'}})
    target = ROOT/'analysis/EDA_gasto_educativo.ipynb'
    nbformat.write(nb,target)
    if not args.no_execute:
        with tempfile.TemporaryDirectory(prefix='cisterna-kernel-') as tmp:
            kernel = Path(tmp)/'kernels'/'cisterna-eda'
            kernel.mkdir(parents=True)
            (kernel/'kernel.json').write_text(json.dumps({
                'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],
                'display_name':'La Cisterna EDA','language':'python',
                'env':{'MPLCONFIGDIR':str(Path(tmp)/'mpl'),'IPYTHONDIR':str(Path(tmp)/'ipython')}}))
            old = os.environ.get('JUPYTER_PATH')
            os.environ['JUPYTER_PATH'] = tmp + (os.pathsep+old if old else '')
            client = NotebookClient(nb,timeout=360,kernel_name='cisterna-eda',resources={'metadata':{'path':str(ROOT/'analysis')}})
            client.on_cell_start = lambda cell,cell_index,**kw: print(f'Celda {cell_index+1}/{len(cells)}: {cell.source.splitlines()[0][:80]}',flush=True)
            try:
                client.execute()
            finally:
                nb.metadata.kernelspec.name='python3'
                nbformat.write(nb,target)
                if old is None: os.environ.pop('JUPYTER_PATH',None)
                else: os.environ['JUPYTER_PATH']=old
        nbformat.validate(nb)
        export_html(nb,ROOT/'analysis/EDA_gasto_educativo.html')
    print(target)

def export_html(nb,target):
    import markdown
    parts=[]
    render=lambda value: markdown.markdown(value,extensions=['tables','fenced_code','toc'])
    for cell in nb.cells:
        if cell.cell_type=='markdown': parts.append('<section>'+render(cell.source)+'</section>')
        else:
            parts.append('<details><summary>Ver código de esta etapa</summary><pre>'+html.escape(cell.source)+'</pre></details>')
            for output in cell.get('outputs',[]):
                data=output.get('data',{})
                if 'image/png' in data: parts.append('<img alt="Gráfico EDA" src="data:image/png;base64,'+data['image/png']+'">')
                elif 'text/html' in data: parts.append('<div class="table">'+data['text/html']+'</div>')
                elif 'text/markdown' in data: parts.append(render(data['text/markdown']))
                elif 'text/plain' in data: parts.append('<pre>'+html.escape(data['text/plain'])+'</pre>')
                elif output.get('output_type')=='stream': parts.append('<pre>'+html.escape(output['text'])+'</pre>')
    css='body{font:17px/1.6 system-ui;color:#203248;max-width:1120px;margin:40px auto;padding:0 24px}h1,h2,h3{line-height:1.25;color:#12495c}h2{border-top:2px solid #d8e4e7;padding-top:32px;margin-top:48px}table{border-collapse:collapse;font-size:13px}th,td{padding:7px 10px;border-bottom:1px solid #dbe3e9;text-align:left}th{background:#e9f0f4}img{max-width:100%;height:auto;margin:20px 0}pre{white-space:pre-wrap;font:13px/1.5 monospace;background:#f3f6f8;padding:16px}.table{overflow:auto}details{margin:14px 0;color:#476579}a{color:#126b85}section{margin:24px 0}'
    target.write_text('<!doctype html><html lang="es"><meta charset="utf-8"><title>EDA La Cisterna</title><style>'+css+'</style><body>'+''.join(parts)+'</body></html>')

if __name__=='__main__': main()
