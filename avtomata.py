import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, QPoint, QTimer, QRect
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont, QPolygon, QIcon

class FiniteAutomata(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(500, 300, 900, 600)
        self.setWindowTitle("Finite Automata")
        self.setWindowIcon(QIcon("image.jpg"))

        self.states = {}
        self.current_step = 0
        self.path = []
        self.accepted = False

        self.initUI()

    def initUI(self):
        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText("Enter binary string...")
        self.line_edit.move(30, 20)
        self.line_edit.resize(350, 45)

        self.start_button = QPushButton("Start", self)
        self.start_button.move(400, 20)
        self.start_button.resize(100, 45)
        self.start_button.clicked.connect(self.start_automaton)

        self.states['q1'] = self.createStateLabel("q1", 100, 250)
        self.states['q2'] = self.createStateLabel("q2", 300, 100)
        self.states['q3'] = self.createStateLabel("q3", 550, 250)
        self.states['q4'] = self.createStateLabel("q4", 300, 400)

        self.result_label = QLabel("", self)
        self.result_label.move(30, 520)
        self.result_label.resize(700, 40)

    def createStateLabel(self, name, x, y):
        label = QLabel(name, self)
        label.move(x, y)
        label.setFixedSize(80, 80)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(self.defaultStyle())
        return label

    def defaultStyle(self):
        return """
            QLabel {
                font-size: 24px;
                font-weight: bold;
                border: 3px solid black;
                background-color: #ecf0f1;
                border-radius: 40px;
                color: black;
            }
        """

    def highlightStyle(self):
        return """
            QLabel {
                font-size: 24px;
                font-weight: bold;
                border: 3px solid orange;
                background-color: yellow;
                border-radius: 40px;
                color: black;
            }
        """

    def acceptStyle(self):
        return """
            QLabel {
                font-size: 24px;
                font-weight: bold;
                border: 3px solid green;
                background-color: lightgreen;
                border-radius: 40px;
                color: black;
            }
        """

    def errorStyle(self):
        return """
            QLabel {
                font-size: 24px;
                font-weight: bold;
                border: 3px solid red;
                background-color: tomato;
                border-radius: 40px;
                color: black;
            }
        """

    def start_automaton(self):
        self.resetAllStates()
        self.result_label.setText("")
        self.current_step = 0
        self.accepted = False
        input_string = self.line_edit.text().strip()

        if not all(c in '01' for c in input_string):
            self.result_label.setText("❌ Invalid input: only 0 and 1 allowed.")
            return

        self.path = self.simulate(input_string)

        self.timer = QTimer()
        self.timer.timeout.connect(self.highlightNextState)
        self.timer.start(700)

    def simulate(self, s):
        current_state = 'q1'
        path = ['q1']

        for char in s:
            if current_state == 'q1':
                current_state = 'q2' if char == '0' else 'q3'
            elif current_state == 'q2':
                current_state = 'q1' if char == '0' else 'q3'
            elif current_state == 'q3':
                current_state = 'q4' if char == '0' else 'q3'
            elif current_state == 'q4':
                break
            path.append(current_state)

        if len(s) > 0 and s[-1] == '0' and path[-1] == 'q4':
            self.accepted = True
            self.result_label.setText("✅ Accepted")
        else:
            self.result_label.setText("❌ Rejected")

        return path

    def resetAllStates(self):
        for state in self.states.values():
            state.setStyleSheet(self.defaultStyle())

    def highlightNextState(self):
        if self.current_step > 0:
            prev_state = self.path[self.current_step - 1]
            self.states[prev_state].setStyleSheet(self.defaultStyle())

        if self.current_step < len(self.path):
            state_name = self.path[self.current_step]
            self.states[state_name].setStyleSheet(self.highlightStyle())
            self.current_step += 1
        else:
            self.timer.stop()
            final_state = self.path[-1]
            if self.accepted:
                self.states[final_state].setStyleSheet(self.acceptStyle())
            else:
                self.states[final_state].setStyleSheet(self.errorStyle())

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Pride flag background
        pride_colors = [
            QColor("#e40303"),  # Red
            QColor("#ff8c00"),  # Orange
            QColor("#ffed00"),  # Yellow
            QColor("#008026"),  # Green
            QColor("#004dff"),  # Blue
            QColor("#750787")   # Purple
        ]
        stripe_height = self.height() // len(pride_colors)
        for i, color in enumerate(pride_colors):
            painter.fillRect(0, i * stripe_height, self.width(), stripe_height, color)

        # Automaton arrows and structure
        arrow_color = QColor(0, 0, 0)
        text_color = QColor(0, 0, 0)

        pen = QPen(arrow_color, 2)
        painter.setPen(pen)
        painter.setBrush(QBrush(Qt.NoBrush))
        painter.setFont(QFont("Arial", 12, QFont.Bold))

        centers = {
            'q1': QPoint(140, 290),
            'q2': QPoint(340, 140),
            'q3': QPoint(590, 290),
            'q4': QPoint(340, 440),
        }

        radius = 40

        def draw_arrow(start, end, text, offset_x=0, offset_y=0):
            dx = end.x() - start.x()
            dy = end.y() - start.y()
            length = math.hypot(dx, dy)
            if length == 0:
                return
            offset_x1 = radius * dx / length
            offset_y1 = radius * dy / length
            line_start = QPoint(int(start.x() + offset_x1), int(start.y() + offset_y1))
            line_end = QPoint(int(end.x() - offset_x1), int(end.y() - offset_y1))
            painter.drawLine(line_start, line_end)
            angle = math.atan2(dy, dx)
            arrow_size = 12
            arrow_p1 = QPoint(
                int(line_end.x() - arrow_size * math.cos(angle - math.pi / 6)),
                int(line_end.y() - arrow_size * math.sin(angle - math.pi / 6))
            )
            arrow_p2 = QPoint(
                int(line_end.x() - arrow_size * math.cos(angle + math.pi / 6)),
                int(line_end.y() - arrow_size * math.sin(angle + math.pi / 6))
            )
            painter.setBrush(QBrush(arrow_color))
            painter.drawPolygon(QPolygon([line_end, arrow_p1, arrow_p2]))
            painter.setPen(QPen(text_color))
            text_x = (start.x() + end.x()) // 2 + offset_x
            text_y = (start.y() + end.y()) // 2 + offset_y
            painter.drawText(text_x - 5, text_y + 5, text)

        painter.drawLine(50, 290, 100, 290)
        draw_arrow(QPoint(50, 290), centers['q1'], "")
        draw_arrow(centers['q1'], centers['q2'], "0", -20, -20)
        draw_arrow(centers['q1'], centers['q3'], "1", 20, -20)
        draw_arrow(centers['q2'], centers['q3'], "1", 0, -20)
        draw_arrow(centers['q2'], centers['q1'], "0", 20, 20)
        draw_arrow(centers['q3'], centers['q4'], "0")

        cx, cy = centers['q3'].x(), centers['q3'].y()
        loop_radius = 28
        loop_rect = QRect(cx - loop_radius, cy - radius - loop_radius - 5, 2 * loop_radius, 2 * loop_radius)
        painter.setPen(QPen(arrow_color, 2))
        painter.drawArc(loop_rect, 0 * 16, 360 * 16)

        arrow_tip = QPoint(cx, cy - radius - 5)
        arrow_size = 10
        angle = -math.pi / 2
        p1 = QPoint(
            int(arrow_tip.x() - arrow_size * math.cos(angle - math.pi / 6)),
            int(arrow_tip.y() - arrow_size * math.sin(angle - math.pi / 6))
        )
        p2 = QPoint(
            int(arrow_tip.x() - arrow_size * math.cos(angle + math.pi / 6)),
            int(arrow_tip.y() - arrow_size * math.sin(angle + math.pi / 6))
        )
        painter.setBrush(QBrush(arrow_color))
        painter.drawPolygon(QPolygon([arrow_tip, p1, p2]))
        painter.setPen(QPen(text_color))
        painter.drawText(cx - 10, cy - radius - loop_radius - 10, "1")

        painter.setPen(QPen(arrow_color, 2))
        painter.drawEllipse(centers['q4'], radius + 4, radius + 4)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FiniteAutomata()
    window.show()
    sys.exit(app.exec_())
