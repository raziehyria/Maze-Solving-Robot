from dataclasses import dataclass, field

@dataclass
class MazePath:
    path: list[str] = field(default_factory=list)
    length: int = 0

    def push_move(self, move) -> None:
        self.path.append(move)
        self.length += 1

    def peek_move(self) -> str:
        return self.path[-1]

    def alter_moves(self, new_move) -> None:
        self.path = self.path[:3] + [new_move]
        self.length -= 2

    def get_prev_moves(self) -> list[str]:
        return self.path.pop(), self.path.pop(), self.path.pop()

    def reduce_path(self) -> None:
        if len(self.path) >= 3:
            move3, move2, move1 = self.get_prev_moves()
            moves = move1 + move2 + move3
            if moves == 'SBS':
                self.alter_moves('B')
            elif moves == '':
                pass
    