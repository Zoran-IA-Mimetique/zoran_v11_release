""" Immutable Hash Log (minimal) """

import hashlib, json, time
class SecureLogger:
    def __init__(self, logger_id: str): self.chain=[]; self._add('INIT',{'id':logger_id},prev='0'*64)
    def _calc(self, b): return hashlib.sha256(json.dumps(b, sort_keys=True).encode()).hexdigest()
    def _add(self, event, details, prev=None):
        prev = prev or self.chain[-1]['hash']
        block={'ts':time.time(),'event':event,'details':details,'prev':prev}
        block['hash']=self._calc(block); self.chain.append(block)
    def log(self, event, details): self._add(event, details)
    def verify_chain(self):
        for i in range(1,len(self.chain)):
            if self.chain[i]['prev']!=self.chain[i-1]['hash']: return False
            if self._calc({k:v for k,v in self.chain[i].items() if k!='hash'})!=self.chain[i]['hash']: return False
        return True
