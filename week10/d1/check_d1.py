"""Real local D1 HTTP/restart acceptance; run after npm ci from this folder."""
import json
import os
from pathlib import Path
import subprocess
import time
from urllib import request,error

ROOT=Path(__file__).resolve().parent
ENV={**os.environ,'WRANGLER_SEND_METRICS':'false'}
CLI=['node',str(ROOT/'node_modules/wrangler/bin/wrangler.js')]
PERSIST=[]

def command(*args):
    subprocess.run(CLI+list(args)+PERSIST,cwd=ROOT,env=ENV,check=True,stdout=subprocess.DEVNULL)

def get(query,status=200):
    try:
        with request.build_opener(request.ProxyHandler({})).open(
                'http://127.0.0.1:8010/messages?conversation='+query,timeout=2) as response:
            assert response.status==status
            return json.load(response)
    except error.HTTPError as exc:
        assert exc.code==status,(exc.code,status)
        return json.load(exc)

def start(log):
    process=subprocess.Popen(['uv','run','--locked','pywrangler']+['dev','--local','--ip','127.0.0.1','--port','8010']+PERSIST,
                             cwd=ROOT,env=ENV,stdout=log,stderr=log)
    for _ in range(180):
        if process.poll() is not None:
            raise RuntimeError('Worker exited:\n' + (ROOT/'d1-check.log').read_text())
        try:
            result=get('1')
            if result.get('success'):return process
        except (OSError,AssertionError):pass
        time.sleep(.5)
    process.terminate();process.wait(timeout=10)
    raise RuntimeError('Worker not ready in 90s:\n' + (ROOT/'d1-check.log').read_text())

def stop(process):
    process.terminate()
    try:process.wait(timeout=10)
    except subprocess.TimeoutExpired:process.kill();process.wait()

if __name__=='__main__':
    # Separate disposable store, never erase a student's working state.
    import tempfile
    with tempfile.TemporaryDirectory(prefix='d1-check-') as temporary:
        PERSIST[:]=['--persist-to',temporary]
        command('d1','execute','sd5913-week10-local','--local','--file','schema.sql')
        process=None
        with open(ROOT/'d1-check.log','w') as log:
            try:
                process=start(log)
                assert len(get('1')['results'])==2
                assert get('999')['results']==[]
                assert 'error' in get('bad',400)
                assert 'error' in get('1%20OR%201=1',400)
                command('d1','execute','sd5913-week10-local','--local','--command',
                        "UPDATE conversation SET title='Restart check' WHERE id=1")
                stop(process);process=None;process=start(log)
                assert all(row['title']=='Restart check' for row in get('1')['results'])
                print('PASS real Python Worker: bound JOIN, bad input, empty result and D1 restart persistence')
            finally:
                if process:stop(process)
