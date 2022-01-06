class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        message: str = (f'Тип тренировки: {self.training_type}; '
                        f'Длительность: {self.duration:-.3f} ч.; '
                        f'Дистанция: {self.distance:-.3f} км; '
                        f'Ср. скорость: {self.speed:-.3f} км/ч; '
                        f'Потрачено ккал: {self.calories:-.3f}.')
        return message


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    TRAINING_TYPE: str = 'Training'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        self.distance: float = (self.action * self.LEN_STEP) / self.M_IN_KM
        return self.distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.mean_speed: float = self.get_distance() / self.duration
        return self.mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.TRAINING_TYPE,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    TRAINING_TYPE: str = 'Running'
    COEFF_CAL_1: int = 18
    COEFF_CAL_2: int = 20
    H_TO_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)
        self.distance = self.get_distance()
        self.mean_speed = self.get_mean_speed()
        self.calories = self.get_spent_calories()

    def get_spent_calories(self) -> float:
        self.calories: float = ((self.COEFF_CAL_1 * self.mean_speed
                                - self.COEFF_CAL_2)
                                * self.weight / self.M_IN_KM
                                * (self.duration * self.H_TO_MIN))
        return self.calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    TRAINING_TYPE: str = 'SportsWalking'
    COEFF_CAL_1: float = 0.035
    COEFF_CAL_2: float = 0.029
    COEFF_CAL_3: int = 2
    H_TO_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.distance = self.get_distance()
        self.mean_speed = self.get_mean_speed()
        self.calories = self.get_spent_calories()

    def get_spent_calories(self) -> float:
        self.calories: float = ((self.COEFF_CAL_1 * self.weight
                                + (self.mean_speed ** self.COEFF_CAL_3
                                 // self.height)
                                * self.COEFF_CAL_2 * self.weight)
                                * (self.duration * self.H_TO_MIN))
        return self.calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_CAL_1: float = 1.1
    COEFF_CAL_2: int = 2
    TRAINING_TYPE: str = 'Swimming'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.distance = self.get_distance()
        self.mean_speed = self.get_mean_speed()
        self.calories = self.get_spent_calories()

    def get_mean_speed(self) -> float:
        self.mean_speed: float = (self.length_pool * self.count_pool
                                  / self.M_IN_KM / self.duration)
        return self.mean_speed

    def get_spent_calories(self) -> float:
        self.calories = ((self.mean_speed + self.COEFF_CAL_1)
                         * self.COEFF_CAL_2 * self.weight)
        return self.calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    training = workout_types[workout_type](*data)
    return training


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
