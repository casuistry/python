import random

class BoardState:
    def __init__(self):
        self.boardState = dict()
        for x in range(1, 9):
            for y in range(1, 9):
                self.boardState[(x,y)] = None
        self.initialize()

    def initialize(self):
        self.boardState[(1,5)] = (Piece.White, Piece.King)
        self.boardState[(8,5)] = (Piece.Black, Piece.King)

        self.boardState[(1,2)] = (Piece.White, Piece.Knight)
        self.boardState[(1,7)] = (Piece.White, Piece.Knight)
        self.boardState[(8,2)] = (Piece.Black, Piece.Knight)
        self.boardState[(8,7)] = (Piece.Black, Piece.Knight)

        self.boardState[(1,3)] = (Piece.White, Piece.Bishop)
        self.boardState[(1,6)] = (Piece.White, Piece.Bishop)
        self.boardState[(8,3)] = (Piece.Black, Piece.Bishop)
        self.boardState[(8,6)] = (Piece.Black, Piece.Bishop)

        self.boardState[(1,1)] = (Piece.White, Piece.Rook)
        self.boardState[(1,8)] = (Piece.White, Piece.Rook)
        self.boardState[(8,1)] = (Piece.Black, Piece.Rook)
        self.boardState[(8,8)] = (Piece.Black, Piece.Rook)

        self.boardState[(1,4)] = (Piece.White, Piece.Queen)
        self.boardState[(8,4)] = (Piece.Black, Piece.Queen)

    def printme(self):
        for x in reversed(range(1, 9)):
            print([self.describe((x,y)) for y in range(1, 9)])
        print()

    def describe(self, pos):
        if not self.boardState[pos]:
            return (' ', ' ')
        else:
            return self.boardState[pos]

    def mutate(self, oldpos, newpos):
        v = self.boardState[oldpos]
        self.boardState[oldpos] = None
        self.boardState[newpos] = v

    def canMove(self, color, pos):
        if pos in self.boardState:
            p = self.boardState[pos]
            if not p:
                return (True, True)
            if p and p[0] != color:
                return (True, False)
        return (False, False)

    def find(self, color, piece):
        for k, v in self.boardState.items():
            if v == (color, piece):
                return k

    def isCheck(self, color):
        opponentcolor = Piece.White if color == Piece.Black else Piece.Black
        kingpos = self.find(color, Piece.King)

        #all except pawn move (only take)
        moves = {k:Piece.getMoves(k,v,self.canMove) for k,v in self.boardState.items() if v and v[0] == opponentcolor}

        res = set()
        for v in moves.values():
            for m in v:
                res.add(m)

        return kingpos in res

    def copyme(self):
        board = BoardState()
        board.boardState = dict(self.boardState)
        return board

    def getMutations(self, color):

        #all moves, including pawn move and take
        moves = {k:Piece.getMoves(k,v, self.canMove) for k,v in self.boardState.items() if v and v[0] == color}

        #check if one of the moves results in king being in check
        valid = dict()
        for k,v in moves.items():
            goodmoves = []
            for m in v:
                newboard = self.copyme()
                newboard.mutate(k, m)
                if not newboard.isCheck(color):
                    #all good
                    goodmoves.append(m)
            if goodmoves:
                valid[k] = goodmoves
        return valid

class Piece:
    White = 'w'
    Black = 'b'
    Pawn = 'P'
    Rook = 'R'
    Knight = 'N'
    Bishop = 'B'
    Queen = 'Q'
    King = 'K'

    @staticmethod
    def walk(pos, delta, color, res, callback):
        nextpos = (pos[0]+delta[0], pos[1]+delta[1])
        accept, more = callback(color, nextpos)
        if accept:
            res.append(nextpos)
        if more:
            Piece.walk(nextpos, delta, color, res, callback)            
        return res

    @staticmethod
    def allMoves(pos, item, callback):
        res = Piece.getMoves(pos, item, callback)
        #add pawn moves (in addition to takes), move by 2 if not moved
        return res

    @staticmethod
    def getMoves(pos, item, callback):
        x,y = pos
        color, piece = item

        if piece == Piece.King:
            #castle if not moved and not under check and .....
            all = [(x-1, y), (x+1, y), (x, y-1), (x, y+1), 
                   (x-1, y-1), (x+1, y-1), (x-1, y+1), (x+1, y+1)]
            return [x for x in all if callback(color, x)[0] == True]
        if piece == Piece.Knight:
            all = [(x-2, y-1), (x-2, y+1), (x+2, y-1), (x+2, y+1), 
                   (x-1, y-2), (x-1, y+2), (x+1, y-2), (x+1, y+2)]
            return [x for x in all if callback(color, x)[0] == True]  
        if piece == Piece.Bishop:
            res = Piece.walk(pos, (1, 1), color, [], callback)
            res.extend(Piece.walk(pos, (-1, 1), color, [], callback))
            res.extend(Piece.walk(pos, (-1, -1), color, [], callback))
            res.extend(Piece.walk(pos, (1, -1), color, [], callback))
            return res   
        if piece == Piece.Rook:
            res = Piece.walk(pos, (0, 1), color, [], callback)
            res.extend(Piece.walk(pos, (0, -1), color, [], callback))
            res.extend(Piece.walk(pos, (-1, 0), color, [], callback))
            res.extend(Piece.walk(pos, (1, 0), color, [], callback))
            return res   
        if piece == Piece.Queen:
            res = Piece.getMoves(pos, (color, Piece.Bishop), callback) 
            res.extend(Piece.getMoves(pos, (color, Piece.Rook), callback))  
            return res    
        #add pawn takes
        return []

class Board:
    def __init__(self):
        self.state = BoardState()

    def move(self, color):
        all = self.state.getMutations(color)
        #{(8, 8): [(7, 8), (8, 7), (7, 7)]}
        if all:
            oldpos, moves = random.choice(list(all.items()))
            newpos = random.choice(moves)
            self.state.mutate(oldpos, newpos)
            return True

        return False

    def play(self):
        for i in range(100):
            print(i)
            if not self.move(Piece.White):
                print("White cannot move")
                break
            else:
                self.state.printme()

            if not self.move(Piece.Black):
                print("Black cannot move")
                break
            else:
                self.state.printme()

b = Board()
b.play()