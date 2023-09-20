import random
import tkinter as tk
import chess
import chess.engine

# Configuration Variables
ROOT_FOLDER = "images/"
PIECE_SIZE = 128
BOARD_SIZE = 8 * PIECE_SIZE
STOCKFISH_PATH = "/usr/local/bin/stockfish"  # Replace with the path to your Stockfish binary


def ai_engine(board, ai_type="random"):
    ai_type = selected_ai_type.get()
    if ai_type == "random":
        legal_moves = list(board.legal_moves)
        if legal_moves:
            move = random.choice(legal_moves)
            board.push(move)
    elif ai_type == "stockfish":
        engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        result = engine.play(board, chess.engine.Limit(time=0.1))
        board.push(result.move)
        engine.quit()


def handle_click(event):
    global selected_piece, board

    x, y = event.x // PIECE_SIZE, event.y // PIECE_SIZE
    square = chess.square(x, 7 - y)

    if selected_piece:
        move = chess.Move.from_uci(f"{selected_piece}{chess.SQUARE_NAMES[square]}")
        if move in board.legal_moves:
            board.push(move)
            draw_board(canvas, board)
            ai_engine(board, ai_type="stockfish")
            draw_board(canvas, board)

        selected_piece = None

    else:
        piece = board.piece_at(square)
        if piece:
            selected_piece = chess.SQUARE_NAMES[square]

    # Update message label
    if board.is_checkmate():
        message_label.config(text="Checkmate! Game Over.", fg="red")
    elif board.is_check():
        message_label.config(text="Check!", fg="blue")
    else:
        message_label.config(text="", fg="black")


def draw_board(canvas, board):
    dark_color = "#D18B47"
    light_color = "#FFCE9E"
    color = light_color
    for i in range(8):
        for j in range(8):
            canvas.create_rectangle(i * PIECE_SIZE, j * PIECE_SIZE,
                                    i * PIECE_SIZE + PIECE_SIZE, j * PIECE_SIZE + PIECE_SIZE, fill=color)
            color = dark_color if color == light_color else light_color
        color = dark_color if color == light_color else light_color

    for square, piece in board.piece_map().items():
        x, y = chess.square_file(square), chess.square_rank(square)
        image = piece_images[str(piece)]
        canvas.create_image(x * PIECE_SIZE + PIECE_SIZE // 2, (7 - y) * PIECE_SIZE + PIECE_SIZE // 2, image=image)


board = chess.Board()

# Initialize Tkinter window
root = tk.Tk()
root.title("Simple Chess Board")

# Create a frame for the message label and dropdown
control_frame = tk.Frame(root)
control_frame.pack(side=tk.TOP, fill=tk.X)

# Global variable to hold the selected AI type
selected_ai_type = tk.StringVar(root)
selected_ai_type.set("random")  # default value

# Create a label for the dropdown
dropdown_label = tk.Label(control_frame, text="AI Type:", font=("Helvetica", 15))
dropdown_label.grid(row=0, column=0)

# Create dropdown for AI type selection
ai_type_dropdown = tk.OptionMenu(control_frame, selected_ai_type, "random", "stockfish")
ai_type_dropdown.grid(row=0, column=1)

# Create a label for displaying messages
message_label = tk.Label(control_frame, text="", font=("Helvetica", 15))
message_label.grid(row=0, column=2)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

start_x = int((screen_width - BOARD_SIZE) / 2)
start_y = int((screen_height - BOARD_SIZE) / 2)

root.geometry(f"{BOARD_SIZE}x{BOARD_SIZE}+{start_x}+{start_y}")

canvas = tk.Canvas(root, width=BOARD_SIZE, height=BOARD_SIZE)
canvas.pack()

piece_name_map = {
    'P': 'white-pawn',
    'R': 'white-rook',
    'N': 'white-knight',
    'B': 'white-bishop',
    'Q': 'white-queen',
    'K': 'white-king',
    'p': 'black-pawn',
    'r': 'black-rook',
    'n': 'black-knight',
    'b': 'black-bishop',
    'q': 'black-queen',
    'k': 'black-king'
}

piece_images = {}
for piece_char, piece_name in piece_name_map.items():
    piece_images[piece_char] = tk.PhotoImage(file=f"{ROOT_FOLDER}{piece_name}.png")

selected_piece = None

canvas.bind("<Button-1>", handle_click)

draw_board(canvas, board)

root.mainloop()
