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

    LEN_STEP = 0.65
    M_IN_KM = 1000
    training_type = 'Training'

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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        self.distance = self.get_distance()
        self.mean_speed = self.get_mean_speed()
        self.calories = self.get_spent_calories()
        info = InfoMessage(self.training_type,
                           self.duration,
                           self.distance,
                           self.mean_speed,
                           self.calories)
        return info


class Running(Training):
    """Тренировка: бег."""
    training_type = 'Running'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)
        self.distance = self.get_distance()
        self.mean_speed = self.get_mean_speed()
        self.calories = self.get_spent_calories()

    def get_spent_calories(self) -> float:
        coeff_cal_1 = 18
        coeff_cal_2 = 20
        self.calories: float = ((coeff_cal_1 * self.mean_speed - coeff_cal_2)
                                * self.weight / self.M_IN_KM
                                * (self.duration * 60))
        return self.calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    training_type = 'SportsWalking'

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
        coeff_cal_1 = 0.035
        coeff_cal_2 = 0.029
        self.calories: float = ((coeff_cal_1 * self.weight
                                + (self.mean_speed ** 2 // self.height)
                                * coeff_cal_2 * self.weight)
                                * (self.duration * 60))
        return self.calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    training_type = 'Swimming'

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
        self.mean_speed = (self.length_pool * self.count_pool / self.M_IN_KM
                           / self.duration)
        return self.mean_speed

    def get_spent_calories(self) -> float:
        coeff_cal_1 = 1.1
        coeff_cal_2 = 2
        self.calories = ((self.mean_speed + coeff_cal_1)
                         * coeff_cal_2 * self.weight)
        return self.calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    workout_types = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    training = workout_types[workout_type](*data)
    return training


def main(training: Training) -> None:
    """Главная функция."""

    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
