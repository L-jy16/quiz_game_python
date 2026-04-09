import json
from quiz import Quiz


class QuizGame:
    def __init__(self):
        self.state_file = "state.json"
        self.quizzes = []
        self.best_score = 0
        self.load_state()

# json 안에 내용이 없을 경우를 위한 기본 데이터
    def get_default_quizzes(self):
        return [
            Quiz("대한민국의 수도는 어디인가요?", ["부산", "서울", "인천", "대전"], 2),
            Quiz("지구에서 가장 큰 대륙은 무엇인가요?", ["아프리카", "유럽", "아시아", "남아메리카"], 3),
            Quiz("물의 화학식은 무엇인가요?", ["CO2", "H2O", "O2", "NaCl"], 2),
            Quiz("태양은 무엇으로 이루어진 천체인가요?", ["고체", "액체", "기체", "플라즈마"], 4),
            Quiz("대한민국의 국기는 무엇인가요?", ["성조기", "유니언잭", "태극기", "오성홍기"], 3),
            Quiz("컴퓨터의 중앙처리장치를 무엇이라고 하나요?", ["RAM", "CPU", "SSD", "GPU"], 2)
        ]

    def load_state(self):
        try:
            # state.json이 있을 경우에 state.json파일을 만듦
            with open(self.state_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            quizzes_data = data.get("quizzes", [])
            self.quizzes = [Quiz.from_dict(item) for item in quizzes_data]
            self.best_score = data.get("best_score", 0)

            if not self.quizzes:
                print("저장된 퀴즈가 없어 기본 퀴즈를 불러옵니다.")
                self.quizzes = self.get_default_quizzes()
                self.save_state()
            else:
                print(f"저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)")

        except FileNotFoundError:
            print("state.json 파일이 없어 기본 퀴즈를 생성합니다.")
            self.quizzes = self.get_default_quizzes()
            self.best_score = 0
            self.save_state()

        except json.JSONDecodeError:
            print("state.json 파일이 손상되어 기본 퀴즈로 복구합니다.")
            self.quizzes = self.get_default_quizzes()
            self.best_score = 0
            self.save_state()

        except Exception as error:
            print(f"파일을 불러오는 중 오류가 발생했습니다: {error}")
            print("기본 퀴즈로 시작합니다.")
            self.quizzes = self.get_default_quizzes()
            self.best_score = 0

    def save_state(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score
        }

        try:
            with open(self.state_file, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        except Exception as error:
            print(f"파일 저장 중 오류가 발생했습니다: {error}")

    def get_int_input(self, prompt, min_value, max_value):
        while True:
            try:
                user_input = input(prompt).strip()

                if user_input == "":
                    print("빈 입력은 허용되지 않습니다. 다시 입력하세요.")
                    continue

                number = int(user_input)

                if number < min_value or number > max_value:
                    print(f"{min_value}부터 {max_value} 사이의 숫자를 입력하세요.")
                    continue

                return number

            except ValueError:
                print("숫자로 입력해야 합니다. 다시 입력하세요.")
            except KeyboardInterrupt:
                print("\n입력이 중단되었습니다. 프로그램을 안전하게 종료합니다.")
                self.save_state()
                raise SystemExit
            except EOFError:
                print("\n입력 스트림이 종료되었습니다. 프로그램을 안전하게 종료합니다.")
                self.save_state()
                raise SystemExit

    def show_menu(self):
        print("\n========================================")
        print(" 나만의 퀴즈 게임 ")
        print("========================================")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("========================================")

    def play_quiz(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print(f"\n 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")
        score = 0

        for index, quiz in enumerate(self.quizzes, start=1):
            print("----------------------------------------")
            quiz.display(index)
            user_answer = self.get_int_input("정답 입력 (1-4): ", 1, 4)

            if quiz.is_correct(user_answer):
                print("정답입니다!")
                score += 1
            else:
                correct_answer_text = quiz.choices[quiz.answer - 1]
                print(f" 오답입니다. 정답은 {quiz.answer}번 ({correct_answer_text}) 입니다.")

        final_score = int((score / len(self.quizzes)) * 100)
        print("========================================")
        print(f"결과: {len(self.quizzes)}문제 중 {score}문제 정답! ({final_score}점)")

        if final_score > self.best_score:
            self.best_score = final_score
            self.save_state()
            print("새로운 최고 점수입니다!")

        print("========================================")

    def add_quiz(self):
        print("\n새로운 퀴즈를 추가합니다.")

        try:
            question = input("문제를 입력하세요: ").strip()
            while question == "":
                print("문제는 비워둘 수 없습니다.")
                question = input("문제를 입력하세요: ").strip()

            choices = []
            for i in range(1, 5):
                choice = input(f"선택지 {i}: ").strip()
                while choice == "":
                    print("선택지는 비워둘 수 없습니다.")
                    choice = input(f"선택지 {i}: ").strip()
                choices.append(choice)

            answer = self.get_int_input("정답 번호 (1-4): ", 1, 4)

            new_quiz = Quiz(question, choices, answer)
            self.quizzes.append(new_quiz)
            self.save_state()

            print("퀴즈가 추가되었습니다!")

        except KeyboardInterrupt:
            print("\n퀴즈 추가가 중단되었습니다.")
            self.save_state()
        except EOFError:
            print("\n퀴즈 추가가 종료되었습니다.")
            self.save_state()

    def show_quiz_list(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("----------------------------------------")
        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"[{i}] {quiz.question}")
        print("----------------------------------------")

    def show_best_score(self):
        if self.best_score == 0:
            print("아직 기록된 최고 점수가 없습니다.")
        else:
            print(f"최고 점수: {self.best_score}점")

    def run(self):
        while True:
            self.show_menu()
            choice = self.get_int_input("선택: ", 1, 5)

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quiz_list()
            elif choice == 4:
                self.show_best_score()
            elif choice == 5:
                self.save_state()
                print("프로그램을 종료합니다.")
                break