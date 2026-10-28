"""No-API checks of the normal prerequisite and changes to its task contract."""
from pathlib import Path
from tempfile import TemporaryDirectory
from copy import deepcopy
from dynamic_arena import OUT
from dynamic_arena.run import open_session,gate,task_digest
from dynamic_arena.tool_arena import PROTOCOL
from expansion_v7.build import write


def main():
    cid='QI:horizontal::dynamic-shortage'
    with TemporaryDirectory() as tmp:
        n=open_session(cid,Path(tmp)/'n','model:test',True);i=open_session(cid,Path(tmp)/'i','model:test',False)
        proof=dict(success=True,caseId=cid,actor='model:test',arenaProtocol=PROTOCOL,arenaBranch='normal',taskDigest=task_digest(n,30))
        assert gate(proof,i,'model:test',30)
        assert not gate(proof,i,'model:other',30) and not gate(proof,i,'model:test',31)
        assert not gate({**proof,'success':False},i,'model:test',30)
        assert not gate({**proof,'caseId':'another-task'},i,'model:test',30)
        available=set(i.ep.runtime.available);i.ep.runtime.available.remove(next(iter(available)))
        assert not gate(proof,i,'model:test',30)
    write(OUT/'normal-prerequisite-check.json',dict(passed=True,apiCalls=0,checks=['same task and model accepted','different model rejected','different budget rejected','failed normal rejected','different case rejected','changed available inventory rejected']))
    print('PASS same-case normal prerequisite and model/budget/inventory mismatches')


if __name__=='__main__':main()
