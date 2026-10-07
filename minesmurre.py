#!/usr/bin/env python3
"""Minesmurre: offline mines puzzle with a safe first reveal."""
import argparse,collections,random,sys
class Game:
    def __init__(self,size=8,mines=10,seed=None):
        if type(size) is not int or not 4<=size<=12:raise ValueError('Size must be 4-12.')
        if type(mines) is not int or not 1<=mines<=size*size-9:raise ValueError('Mines must be 1 to size squared minus 9.')
        self.size=size;self.count=mines;self.rng=random.Random(seed);self.mines=None;self.open=set();self.flags=set();self.lost=False;self.actions=0
    def position(self,r,c):
        if type(r) is not int or type(c) is not int or not 0<=r<self.size or not 0<=c<self.size:raise ValueError('Coordinates outside board.')
        return r,c
    def neighbors(self,pos):
        r,c=pos
        return [(nr,nc) for nr in range(max(0,r-1),min(self.size,r+2)) for nc in range(max(0,c-1),min(self.size,c+2)) if (nr,nc)!=pos]
    def place(self,first):
        excluded=set(self.neighbors(first))|{first};pool=[(r,c) for r in range(self.size) for c in range(self.size) if (r,c) not in excluded];self.mines=set(self.rng.sample(pool,self.count))
    def number(self,pos):return sum(p in self.mines for p in self.neighbors(pos)) if self.mines is not None else 0
    def reveal(self,r,c):
        pos=self.position(r,c)
        if self.lost or self.won():raise ValueError('Game already ended.')
        if pos in self.flags:raise ValueError('Remove the flag before revealing.')
        if pos in self.open:return False
        if self.mines is None:self.place(pos)
        self.actions+=1
        if pos in self.mines:self.open.add(pos);self.lost=True;return True
        queue=collections.deque([pos])
        while queue:
            p=queue.popleft()
            if p in self.open or p in self.flags or p in self.mines:continue
            self.open.add(p)
            if self.number(p)==0:queue.extend(self.neighbors(p))
        return True
    def flag(self,r,c):
        pos=self.position(r,c)
        if self.lost or self.won():raise ValueError('Game already ended.')
        if pos in self.open:raise ValueError('Cannot flag a revealed square.')
        if pos in self.flags:self.flags.remove(pos)
        else:
            if len(self.flags)>=self.count:raise ValueError('Flag limit reached. Remove another flag first.')
            self.flags.add(pos)
        self.actions+=1
    def won(self):return self.mines is not None and not self.lost and len(self.open)==self.size*self.size-self.count
    def display(self,reveal_all=False):
        print('\nMINESMURRE | ? hidden | F flag | . zero | * mine')
        print('    '+' '.join(f'{c+1:2}' for c in range(self.size)))
        for r in range(self.size):
            cells=[]
            for c in range(self.size):
                pos=(r,c)
                if reveal_all and self.mines is not None and pos in self.mines:v='*'
                elif pos in self.flags:v='F'
                elif pos in self.open:v='*' if pos in self.mines else str(self.number(pos)) if self.number(pos) else '.'
                else:v='?'
                cells.append(f'{v:>2}')
            print(f'{r+1:2}  '+' '.join(cells))
        print('Mines:',self.count,'| Flags:',len(self.flags),'| Revealed:',len(self.open),'| Actions:',self.actions)
        print('R row col reveal | F row col toggle flag | Q quit. Coordinates start at 1.')

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--size',type=int,default=8);p.add_argument('--mines',type=int,default=10);p.add_argument('--seed',type=int);p.add_argument('--demo',action='store_true');a=p.parse_args(argv)
    try:
        g=Game(a.size,a.mines,a.seed)
        if a.demo:g.reveal(0,0);g.display();return 0
        print('Offline mines puzzle. First reveal and its neighbors are safe; later guesses may be needed.')
        while True:
            g.display(g.lost)
            if g.lost or g.won():print('Mine hit.' if g.lost else 'All safe squares revealed. Won!');return 0
            text=input('> ').strip().lower()
            if text=='q':return 0
            try:
                parts=text.split()
                if len(parts)!=3 or parts[0] not in ('r','f'):raise ValueError('Use R row col or F row col.')
                r,c=int(parts[1])-1,int(parts[2])-1
                if parts[0]=='r':g.reveal(r,c)
                else:g.flag(r,c)
            except ValueError as exc:print('Error:',exc)
    except (EOFError,KeyboardInterrupt):print('\nBye.')
    except ValueError as exc:print('Error:',exc,file=sys.stderr);return 2
    return 0
if __name__=='__main__':raise SystemExit(main())
