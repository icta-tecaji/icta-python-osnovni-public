class Avto:
    def __init__(self, color) -> None:
        self.speed = 0
        self.max_speed = 200
        self.color = color
        self.engine_started = False

    def start_engine(self) -> None:
        self.engine_started = True

    def stop_engine(self) -> None:
        self.engine_started = False

    def accelerate(self, speed: int) -> None:
        if self.engine_started:
            self.speed += speed
            self.speed = min(self.speed, self.max_speed)
        else:
            print("Start the engine first.")


avto1 = Avto("red")
avto1.start_engine()
avto1.accelerate(100)
print(avto1.speed)

avto2 = Avto("blue")
avto2.start_engine()
