import random

# Definition of direction vectors
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


class Snake:

    def __init__(self, init_body, init_direction):
        # Instantiation with body (list of tuples) and moving direction (one of UP, DOWN, LEFT, RIGHT)
        self.body = init_body
        self.direction = init_direction

    def take_step(self, position):
        # Method to apply changes to the snake as it moves
        self.body = self.body[1:] + [position]

    def set_direction(self, direction):
        # Changing direction of snake
        self.direction = direction

    def head(self):
        # Method to return position of snake head
        return self.body[-1]


class Apple:

    def __init__(self, init_position):
        # Instantiation with position
        self.position = init_position

    def set_position(self, position):
        # Method to set apple position
        self.position = position


class Game:
    EMPTY = 0
    BODY = 1
    HEAD = 2
    APPLE = 3

    DISPLAY_CHARS = {
        EMPTY: " ",
        BODY: "O",
        HEAD: "X",
        APPLE: "A",
    }

    KEYBOARD_DIR = {
        "W": UP,
        "S": DOWN,
        "A": LEFT,
        "D": RIGHT
    }

    def __init__(self, height, width):
        # Instantiation of game with given height and width

        self.height = height
        self.width = width

        # Fixed snake starting position - can probably be randomized
        self.snake = Snake([(0, 0),
                            (1, 0),
                            (2, 0),
                            (3, 0),
                            (4, 0)], DOWN)

        apple_pos = random.choice(self.possible_apple_coords())
        self.apple = Apple(apple_pos)
        self.score = 0

    def possible_apple_coords(self):
        # Method to return list of tuples with possible coordinates for the apple
        coords = []
        for i in range(self.height):
            for j in range(self.width):
                coords.append((i, j))

        for x in self.snake.body:
            coords.remove(x)

        if coords:
            return coords
        else:
            return None

    def board_matrix(self):
        # Method to return board matrix with positions of snake and apple
        self.board = [[self.EMPTY for x in range(self.width)] for x in range(self.height)]
        for coord in self.snake.body:
            self.board[coord[0]][coord[1]] = self.BODY

        head_coord = self.snake.head()
        self.board[head_coord[0]][head_coord[1]] = self.HEAD

        apple_coord = self.apple.position
        self.board[apple_coord[0]][apple_coord[1]] = self.APPLE

        return self.board

    def render(self):
        # Method to render the matrix in the terminal
        matrix = self.board_matrix()
        for i in range(self.height + 2):
            if i == 0 or i == self.height + 1:
                print("+" + "-" * self.width + "+")
            else:
                newstring = ""
                for j in range(self.width):
                    newstring += self.DISPLAY_CHARS[matrix[i - 1][j]]
                print("|" + newstring + "|")

    def play(self):
        # Method to play snake
        self.render()

        while True:
            player_input = input().upper()
            if player_input in ["W", "S", "A", "D"]:
                new_direction = self.KEYBOARD_DIR[player_input]
                if new_direction != (self.snake.direction[0] * -1, self.snake.direction[1] * -1):
                    self.snake.set_direction(new_direction)


            newposition = (
                (self.snake.head()[0] + self.snake.direction[0]) % self.height,
                (self.snake.head()[1] + self.snake.direction[1]) % self.width
            )

            if newposition in self.snake.body:
                print(f"GAME OVER\nScore: {self.score}")
                break

            if newposition == self.apple.position:
                self.snake.body.append(self.apple.position)
                self.score += 1

                possiblecoords = self.possible_apple_coords()

                if possiblecoords == None:
                    print(f"You Won!\nScore: {self.score}")
                    break

                newapple = random.choice(possiblecoords)
                self.apple.set_position(newapple)

            else:
                self.snake.take_step(newposition)

            self.render()


newgame = Game(5, 10)

newgame.play()
