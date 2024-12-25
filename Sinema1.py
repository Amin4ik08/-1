class User:
    def __init__(self, username, password):
        # Инициализация пользователя с именем пользователя и паролем
        self.username = username
        self.password = password


class Movie:
    def __init__(self, title, genre, rating, price):
        # Инициализация фильма с заголовком, жанром, рейтингом и ценой
        self.title = title
        self.genre = genre
        self.rating = rating
        self.price = price


class Admin(User):
    def __init__(self, username, password):
        # Инициализация администратора, который является пользователем
        super().__init__(username, password)

    def view_user_history(self, patron):
        # Метод для просмотра истории покупок пользователя
        if patron.history:
            print(f"История покупок для пользователя {patron.username}:")
            for movie in patron.history:
                print(f"{movie.title}, Жанр: {movie.genre}, Рейтинг: {movie.rating}, Цена: ${movie.price}")
        else:
            print(f"У пользователя {patron.username} нет истории покупок.")

    def analyze_statistics(self, cinema):
        # Метод для анализа статистики
        total_users = len(cinema.users)
        total_movies = len(cinema.movies)
        print(f"Общее количество пользователей: {total_users}")
        print(f"Общее количество фильмов: {total_movies}")

        # Подсчет популярности фильмов
        movie_popularity = {}
        for user in cinema.users:
            if isinstance(user, Patron):
                for movie in user.history:
                    if movie.title in movie_popularity:
                        movie_popularity[movie.title] += 1
                    else:
                        movie_popularity[movie.title] = 1

        print("Популярность фильмов:")
        for title, count in movie_popularity.items():
            print(f"{title}: {count} покупок")


class Patron(User):
    def __init__(self, username, password):
        # Инициализация патрона, который является пользователем
        super().__init__(username, password)
        self.history = []  # История покупок
        self.cart = []  # Корзина для покупок

    def purchase_movie(self, movie):
        # Метод для покупки фильма
        self.history.append(movie)

    def add_to_cart(self, movie):
        # Метод для добавления фильма в корзину
        self.cart.append(movie)


class Cinema:
    def __init__(self):
        # Инициализация кинотеатра с пользователями и фильмами
        self.users = []  # Список пользователей
        self.movies = []  # Список фильмов
        self.current_user = None  # Текущий пользователь

    def register_user(self, username, password, is_admin=False):
        # Метод регистрации пользователя (администратор или патрон)
        if any(user.username == username for user in self.users):
            print("Пользователь с таким именем уже существует.")
            return
        if is_admin:
            self.users.append(Admin(username, password))
        else:
            self.users.append(Patron(username, password))

    def authenticate(self, username, password):
        # Метод аутентификации пользователя
        for user in self.users:
            if user.username == username and user.password == password:
                self.current_user = user
                return True
        return False

    def add_movie(self, title, genre, rating, price):
        # Метод добавления фильма (доступен только администратору)
        if isinstance(self.current_user, Admin):
            self.movies.append(Movie(title, genre, rating, price))
            print(f"Фильм '{title}' добавлен.")
        else:
            print("Доступ запрещен.")

    def remove_movie(self, title):
        # Метод удаления фильма (доступен только администратору)
        if isinstance(self.current_user, Admin):
            self.movies = [movie for movie in self.movies if movie.title != title]
            print(f"Фильм '{title}' удален.")
        else:
            print("Доступ запрещен.")

    def list_movies(self):
        # Метод для отображения списка фильмов
        if not self.movies:
            print("Нет доступных фильмов.")
            return
        for movie in self.movies:
            print(f"{movie.title}, Жанр: {movie.genre}, Рейтинг: {movie.rating}, Цена: ${movie.price}")

    def filter_movies(self, genre=None, min_rating=None):
        # Метод для фильтрации фильмов по жанру и минимальному рейтингу
        filtered_movies = self.movies
        if genre:
            filtered_movies = [m for m in filtered_movies if m.genre.lower() == genre.lower()]
        if min_rating is not None:
            filtered_movies = [m for m in filtered_movies if m.rating >= min_rating]
        if filtered_movies:
            for movie in filtered_movies:
                print(f"{movie.title}, Жанр: {movie.genre}, Рейтинг: {movie.rating}, Цена: ${movie.price}")
        else:
            print("Нет фильмов, соответствующих вашим критериям.")

    def user_history(self):
        # Метод для отображения истории покупок пользователя
        if isinstance(self.current_user, Patron):
            if not self.current_user.history:
                print("Нет истории покупок.")
                return
            for movie in self.current_user.history:
                print(f"{movie.title}, Жанр: {movie.genre}, Рейтинг: {movie.rating}, Цена: ${movie.price}")

    def update_password(self, new_password):
        # Метод для обновления пароля пользователя
        if self.current_user:
            self.current_user.password = new_password
            print("Пароль успешно обновлен.")

    def manage_users(self):
        # Метод для управления пользователями (доступен только администратору)
        if isinstance(self.current_user, Admin):
            while True:
                print(
                    "1. Добавить пользователя\n2. Удалить пользователя\n3. Изменить данные пользователя\n4. Просмотреть историю покупок пользователя\n5. Вернуться в главное меню")
                choice = input("Выберите опцию: ")

                if choice == "1":
                    username = input("Имя пользователя: ")
                    password = input("Пароль: ")
                    is_admin = input("Является администратором? (да/нет): ").lower() == "да"
                    self.register_user(username, password, is_admin)
                elif choice == "2":
                    username = input("Имя пользователя для удаления: ")
                    self.users = [user for user in self.users if user.username != username]
                    print(f"Пользователь '{username}' удален.")
                elif choice == "3":
                    username = input("Имя пользователя для изменения: ")
                    user = next((u for u in self.users if u.username == username), None)
                    if user:
                        new_username = input("Новое имя пользователя (оставьте пустым для пропуска): ")
                        new_password = input("Новый пароль (оставьте пустым для пропуска): ")
                        if new_username:
                            user.username = new_username
                        if new_password:
                            user.password = new_password
                        print(f"Данные пользователя '{username}' обновлены.")
                    else:
                        print("Пользователь не найден.")
                elif choice == "4":
                    username = input("Имя пользователя для просмотра истории: ")
                    patron = next((u for u in self.users if isinstance(u, Patron) and u.username == username), None)
                    if patron:
                        self.current_user.view_user_history(patron)
                    else:
                        print("Пользователь не найден.")
                elif choice == "5":
                    break

    def user_session(self):
        # Метод для управления сессией пользователя (администратор или патрон)
        while True:
            if isinstance(self.current_user, Admin):
                print(
                    "1. Управление пользователями\n2. Добавить фильм\n3. Удалить фильм\n4. Список фильмов\n5. Анализ статистики\n6. Выйти")
            else:
                print(
                    "1. Список фильмов\n2. Фильтровать фильмы\n3. Купить фильм\n4. История\n5. Изменить пароль\n6. Выйти")
            choice = input("Выберите опцию: ")

            if isinstance(self.current_user, Admin):
                if choice == "1":
                    self.manage_users()
                elif choice == "2":
                    title = input("Название фильма: ")
                    genre = input("Жанр: ")
                    while True:
                        try:
                            rating = float(input("Рейтинг: "))
                            price = float(input("Цена: "))
                            self.add_movie(title, genre, rating, price)
                            break  # Выход из цикла, если ввод корректный
                        except ValueError:
                            print("Пожалуйста, введите корректные значения для рейтинга и цены.")
                elif choice == "3":
                    title = input("Название фильма для удаления: ")
                    self.remove_movie(title)
                elif choice == "4":
                    self.list_movies()
                elif choice == "5":
                    self.current_user.analyze_statistics(self)
                elif choice == "6":
                    break
            else:
                if choice == "1":
                    self.list_movies()
                elif choice == "2":
                    genre = input("Фильтровать по жанру (оставьте пустым для всех): ") or None
                    while True:
                        min_rating = input("Минимальный рейтинг (оставьте пустым для без фильтра): ")
                        try:
                            min_rating = float(min_rating) if min_rating else None
                            self.filter_movies(genre, min_rating)
                            break  # Выход из цикла, если ввод корректный
                        except ValueError:
                            print("Пожалуйста, введите корректное значение для минимального рейтинга.")
                elif choice == "3":
                    title = input("Название фильма для покупки: ")
                    movie = next((m for m in self.movies if m.title == title), None)
                    if movie:
                        self.current_user.purchase_movie(movie)
                        print(f"Куплен '{movie.title}'.")
                    else:
                        print("Фильм не найден.")
                elif choice == "4":
                    self.user_history()
                elif choice == "5":
                    new_password = input("Новый пароль: ")
                    self.update_password(new_password)
                elif choice == "6":
                    break

    def main_menu(self):
        # Основное меню для взаимодействия с пользователем
        while True:
            print("1. Войти\n2. Зарегистрироваться\n3. Выйти")
            choice = input("Выберите опцию: ")

            if choice == "1":
                username = input("Имя пользователя: ")
                password = input("Пароль: ")
                if self.authenticate(username, password):
                    print(f"Добро пожаловать, {self.current_user.username}!")
                    self.user_session()
                else:
                    print("Неверные учетные данные.")
            elif choice == "2":
                username = input("Имя пользователя: ")
                password = input("Пароль: ")
                is_admin = input("Является администратором? (да/нет): ").lower() == "да"
                self.register_user(username, password, is_admin)
                print("Пользователь зарегистрирован.")
            elif choice == "3":
                break


if __name__ == "__main__":
    # Запуск приложения кинотеатра
    cinema_app = Cinema()
    cinema_app.main_menu()