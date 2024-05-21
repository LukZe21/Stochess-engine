import subprocess

stockfish_path = 'stockfish/stockfish_algorithm.exe'

engine = subprocess.Popen(
    stockfish_path, universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE
)

def send_command(command):
    """Send a command to Stockfish."""
    engine.stdin.write(command + "\n")
    engine.stdin.flush()


def get_response():
    """Get a response from Stockfish."""
    response = ""
    while True:
        text = engine.stdout.readline().strip()
        if text == 'readyok':
            break
        response += text + "\n"
    return response

def start_stockfish():
    """Start Stockfish and UCI mode."""
    send_command("uci")
    while True:
        if 'uciok' in engine.stdout.readline():
            break

def set_position(moves):
    """Set the position on the board using a list of moves."""
    send_command(f"position startpos moves {" ".join(moves)}")

def get_best_move():
    """Get the best move from the current position"""
    send_command("go movetime 500")
    while True:
        line = engine.stdout.readline().strip()
        if line.startswith('bestmove'):
            return line.split()[1]
        
def set_skill_level(skill_lvl):
    send_command(f"setoption name Skill Level value {skill_lvl}")

def main():
    # Start the engine and set to UCI mode
    start_stockfish()

    # Set the initial position
    moves = []
    set_position(moves)

    # Play a game where Stockfish plays against itself
    while True:
        best_move = get_best_move()
        if best_move == "(none)":
            break
        print(f"Stockfish's move: {best_move}")
        moves.append(best_move)
        set_position(moves)

    print("Game Over!")
    send_command("quit")


if __name__ == "__main__":
    main()

def stockfish_move(moves_lst):
    set_position(moves_lst)
    best_move = get_best_move()
    print(f"Stockfish 16.1's move: {best_move}")
    moves_lst.append(best_move)

    return best_move