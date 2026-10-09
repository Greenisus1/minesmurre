#!/usr/bin/env python3
"""Minesmurre: offline mines puzzle with a safe first reveal."""
import argparse,collections,random,sys,os
try:import curses
except ImportError:curses=None
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

def plain_main(argv=None):
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


def paint(stdscr,g,cursor,message):
    stdscr.erase();h,w=stdscr.getmaxyx()
    if h<g.size+10 or w<max(56,g.size*4+10):
        stdscr.addnstr(0,0,"Resize terminal (at least %dx%d); Q exits."%(max(56,g.size*4+10),g.size+10),max(0,w-1));stdscr.refresh();return
    cw=max(4,(w-6)//g.size);rh=max(1,(h-10)//g.size);x=(w-g.size*cw)//2;y=5
    stdscr.addstr(1,3," M I N E S M U R R E ",curses.color_pair(1)|curses.A_BOLD)
    stdscr.addstr(2,3,"Reveal the safe squares. First reveal + neighbors are safe.")
    stdscr.addstr(3,3,f"{g.count} mines   {len(g.flags)} flags   {len(g.open)} revealed   {g.actions} moves",curses.color_pair(1))
    for r in range(g.size):
        for c in range(g.size):
            p=r,c;v="?";color=2
            if g.lost and g.mines is not None and p in g.mines:v="*";color=3
            elif p in g.flags:v="F";color=4
            elif p in g.open:
                n=g.number(p);v=str(n) if n else ".";color=1 if n else 2
            style=curses.color_pair(color)|curses.A_BOLD
            if p==cursor:style|=curses.A_REVERSE
            for dy in range(rh):stdscr.addstr(y+r*rh+dy,x+c*cw,v.center(cw-1),style)
    ended=g.lost or g.won()
    text="Mine hit. R starts a new board." if g.lost else "All safe squares revealed. Won! R starts again." if g.won() else message
    stdscr.addnstr(h-4,3,text,w-6,curses.color_pair(3 if g.lost else 4 if g.won() else 1))
    stdscr.addstr(h-3,3,"Arrows / WASD move   Space / Enter reveal   F flag")
    stdscr.addstr(h-2,3,"R new board   Q quit   --plain for typed coordinates")
    stdscr.refresh()
def terminal(stdscr,size,mines,seed):
    curses.curs_set(0)
    if curses.has_colors():
        curses.start_color();curses.use_default_colors()
        for i,fg in enumerate((curses.COLOR_CYAN,curses.COLOR_WHITE,curses.COLOR_RED,curses.COLOR_YELLOW),1):curses.init_pair(i,fg,-1)
    g=Game(size,mines,seed);cursor=(0,0);message="No mines placed yet. Choose a square."
    while True:
        paint(stdscr,g,cursor,message);key=stdscr.getch()
        if key in (ord('q'),ord('Q')):return
        h,w=stdscr.getmaxyx()
        if h<size+10 or w<max(56,size*4+10):continue
        if key in (ord('r'),ord('R')):g=Game(size,mines,seed);cursor=(0,0);message="New board. First reveal is safe.";continue
        delta={curses.KEY_UP:(-1,0),ord('w'):(-1,0),curses.KEY_DOWN:(1,0),ord('s'):(1,0),curses.KEY_LEFT:(0,-1),ord('a'):(0,-1),curses.KEY_RIGHT:(0,1),ord('d'):(0,1)}.get(key)
        if delta:cursor=(max(0,min(size-1,cursor[0]+delta[0])),max(0,min(size-1,cursor[1]+delta[1])))
        elif key in (10,13,32,ord('f'),ord('F')):
            try:
                if key in (ord('f'),ord('F')):g.flag(*cursor);message="Flag toggled."
                else:g.reveal(*cursor);message="Square revealed."
            except ValueError as e:message=str(e)
def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--size',type=int,default=8);p.add_argument('--mines',type=int,default=10);p.add_argument('--seed',type=int);p.add_argument('--plain',action='store_true');p.add_argument('--demo',action='store_true');a=p.parse_args(argv)
    args=['--size',str(a.size),'--mines',str(a.mines)]+(['--seed',str(a.seed)] if a.seed is not None else [])+(['--demo'] if a.demo else [])
    if curses is None or a.plain or a.demo or not sys.stdin.isatty() or not sys.stdout.isatty() or os.environ.get('TERM') in (None,'dumb'):return plain_main(args)
    try:
        Game(a.size,a.mines,a.seed);curses.wrapper(terminal,a.size,a.mines,a.seed);return 0
    except ValueError as e:print(e,file=sys.stderr);return 2
    except curses.error:print('Terminal initialization failed. Retry with --plain.',file=sys.stderr);return 2
    except KeyboardInterrupt:return 0
if __name__=='__main__':raise SystemExit(main())
