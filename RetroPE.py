import os, time, random, msvcrt

def clear():
    os.system("cls")

def getch():
    return msvcrt.getch().decode(errors="ignore").lower()

# ---------- Snake ----------
def snake():
    w,h=30,20
    snake=[(10,10),(9,10),(8,10)]
    dx,dy=1,0
    food=(random.randrange(w),random.randrange(h))
    while True:
        clear()
        print("SNAKE (WASD, Q quit)")
        for y in range(h):
            row=""
            for x in range(w):
                if (x,y)==snake[0]: row+="@"
                elif (x,y) in snake: row+="o"
                elif (x,y)==food: row+="*"
                else: row+=" "
            print(row)
        time.sleep(0.1)
        if msvcrt.kbhit():
            k=getch()
            if k=="q": return
            if k=="w": dx,dy=0,-1
            if k=="s": dx,dy=0,1
            if k=="a": dx,dy=-1,0
            if k=="d": dx,dy=1,0
        hx,hy=snake[0]
        nh=(hx+dx,hy+dy)
        if nh[0]<0 or nh[0]>=w or nh[1]<0 or nh[1]>=h or nh in snake:
            input("Game Over. Enter.")
            return
        snake.insert(0,nh)
        if nh==food:
            food=(random.randrange(w),random.randrange(h))
        else:
            snake.pop()

# ---------- 2048 ----------
def merge(row):
    row=[x for x in row if x]
    i=0
    out=[]
    while i<len(row):
        if i+1<len(row) and row[i]==row[i+1]:
            out.append(row[i]*2); i+=2
        else:
            out.append(row[i]); i+=1
    return out+[0]*(4-len(out))

def add_tile(b):
    e=[(r,c) for r in range(4) for c in range(4) if b[r][c]==0]
    if e:
        r,c=random.choice(e); b[r][c]=2

def move2048(b,d):
    old=[r[:] for r in b]
    if d=="a":
        for r in range(4): b[r]=merge(b[r])
    if d=="d":
        for r in range(4): b[r]=list(reversed(merge(list(reversed(b[r])))))
    if d=="w":
        for c in range(4):
            col=merge([b[r][c] for r in range(4)])
            for r in range(4): b[r][c]=col[r]
    if d=="s":
        for c in range(4):
            col=list(reversed(merge(list(reversed([b[r][c] for r in range(4)])))))
            for r in range(4): b[r][c]=col[r]
    return old!=b

def game2048():
    b=[[0]*4 for _ in range(4)]
    add_tile(b); add_tile(b)
    while True:
        clear(); print("2048 (WASD, Q quit)")
        for r in b: print(" ".join(f"{x:4}" if x else "   ." for x in r))
        k=getch()
        if k=="q": return
        if k in "wasd" and move2048(b,k): add_tile(b)

# ---------- Minesweeper ----------
def minesweeper():
    w=h=8; mines=10
    board=[[0]*w for _ in range(h)]
    cells=[(x,y) for x in range(w) for y in range(h)]
    for x,y in random.sample(cells,mines):
        board[y][x]=-1
    for y in range(h):
        for x in range(w):
            if board[y][x]==-1: continue
            n=0
            for yy in range(max(0,y-1),min(h,y+2)):
                for xx in range(max(0,x-1),min(w,x+2)):
                    n += board[yy][xx]==-1
            board[y][x]=n
    rev=set()
    cx=cy=0
    while True:
        clear()
        print("MINESWEEPER (WASD move, O open, Q quit)")
        for y in range(h):
            row=""
            for x in range(w):
                ch="#"
                if (x,y) in rev: ch="*" if board[y][x]==-1 else str(board[y][x])
                if (x,y)==(cx,cy): row+=f"[{ch}]"
                else: row+=f" {ch} "
            print(row)
        k=getch()
        if k=="q": return
        if k=="w": cy=max(0,cy-1)
        if k=="s": cy=min(h-1,cy+1)
        if k=="a": cx=max(0,cx-1)
        if k=="d": cx=min(w-1,cx+1)
        if k=="o":
            if board[cy][cx]==-1:
                input("BOOM! Enter.")
                return
            rev.add((cx,cy))

# ---------- Tetris ----------
PIECES=[[[1,1,1,1]],[[1,1],[1,1]],[[0,1,0],[1,1,1]]]
def rot(p): return [list(r) for r in zip(*p[::-1])]
def tetris():
    W,H=10,20
    B=[[0]*W for _ in range(H)]

    PIECES=[
        [[1,1,1,1]],
        [[1,1],[1,1]],
        [[0,1,0],[1,1,1]],
        [[1,0,0],[1,1,1]],
        [[0,0,1],[1,1,1]],
        [[0,1,1],[1,1,0]],
        [[1,1,0],[0,1,1]]
    ]

    def rot(p):
        return [list(r) for r in zip(*p[::-1])]

    def coll(piece,px,py):
        for yy,row in enumerate(piece):
            for xx,v in enumerate(row):
                if not v:
                    continue

                bx=px+xx
                by=py+yy

                if bx<0 or bx>=W:
                    return True

                if by>=H:
                    return True

                if by>=0 and B[by][bx]:
                    return True

        return False

    def lock(piece,px,py):
        for yy,row in enumerate(piece):
            for xx,v in enumerate(row):
                if v:
                    B[py+yy][px+xx]=1

    def clear_lines():
        nonlocal B

        keep=[r for r in B if not all(r)]
        removed=H-len(keep)

        while len(keep)<H:
            keep.insert(0,[0]*W)

        B=keep
        return removed

    p=random.choice(PIECES)
    x=3
    y=0

    score=0

    while True:

        clear()
        print("TETRIS  Score:",score)
        print("WASD or Arrow Keys, Q quit")

        D=[r[:] for r in B]

        for py,row in enumerate(p):
            for px,v in enumerate(row):
                if v:
                    by=y+py
                    bx=x+px

                    if 0<=by<H and 0<=bx<W:
                        D[by][bx]=1

        for row in D:
            print("".join("[]" if c else " ." for c in row))

        time.sleep(0.08)

        if msvcrt.kbhit():

            k=msvcrt.getch()

            if k==b'\xe0':
                a=msvcrt.getch()

                if a==b'K':      # left
                    if not coll(p,x-1,y):
                        x-=1

                elif a==b'M':    # right
                    if not coll(p,x+1,y):
                        x+=1

                elif a==b'P':    # down
                    if not coll(p,x,y+1):
                        y+=1

                elif a==b'H':    # up rotate
                    np=rot(p)
                    if not coll(np,x,y):
                        p=np

            else:

                k=k.decode(errors="ignore").lower()

                if k=="q":
                    return

                elif k=="a":
                    if not coll(p,x-1,y):
                        x-=1

                elif k=="d":
                    if not coll(p,x+1,y):
                        x+=1

                elif k=="s":
                    if not coll(p,x,y+1):
                        y+=1

                elif k=="w":
                    np=rot(p)
                    if not coll(np,x,y):
                        p=np

        if coll(p,x,y+1):

            lock(p,x,y)

            score += clear_lines()*100

            p=random.choice(PIECES)
            x=3
            y=0

            if coll(p,x,y):
                clear()
                print("GAME OVER")
                print("Score:",score)
                input("Enter...")
                return

        else:
            y+=1

# ---------- Main App ----------

def menu():
    while True:
        clear()
        print("=== RetroPE Arcade ===")
        print("1. Tetris")
        print("2. Snake")
        print("3. 2048")
        print("4. Minesweeper")
        print("0. Exit")
        k=getch()
        if k=="1": tetris()
        elif k=="2": snake()
        elif k=="3": game2048()
        elif k=="4": minesweeper()
        elif k=="0": break

if __name__ == "__main__":
    menu()