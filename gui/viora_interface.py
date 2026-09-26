import math
import random
import sys

from PyQt6.QtCore import QPointF, QTimer, Qt
from PyQt6.QtGui import (
    QColor,
    QFont,
    QLinearGradient,
    QPainter,
    QPen,
    QRadialGradient,
)
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class HolographicCore(QWidget):
    """Animated golden holographic sphere inspired by the supplied reference."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(520, 520)
        self.angle = 0.0
        self.pulse = 0.0

        random.seed(7)

        # Static particle/ring data so the animation stays lightweight.
        self.particles = []
        for _ in range(850):
            theta = random.uniform(0, math.tau)
            radius = random.uniform(115, 245)
            z = random.uniform(-1.0, 1.0)
            self.particles.append((theta, radius, z, random.uniform(0.35, 1.0)))

        self.rings = []
        for _ in range(22):
            self.rings.append(
                (
                    random.uniform(0, math.tau),
                    random.uniform(0.75, 1.25),
                    random.choice([-1, 1]),
                    random.uniform(0.3, 0.9),
                )
            )

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)

    def animate(self):
        self.angle = (self.angle + 0.7) % 360
        self.pulse += 0.055
        self.update()

    def paintEvent(self, a0):
    
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        w = self.width()
        h = self.height()
        cx = w / 2
        cy = h / 2
        base_radius = min(w, h) * 0.29
        pulse = 1.0 + math.sin(self.pulse) * 0.025
        radius = base_radius * pulse

        # Transparent/very dark background.
        painter.fillRect(self.rect(), QColor(5, 9, 18))

        # Large soft outer glow.
        glow = QRadialGradient(QPointF(cx, cy), radius * 1.45)
        glow.setColorAt(0.0, QColor(255, 180, 35, 48))
        glow.setColorAt(0.45, QColor(255, 145, 15, 22))
        glow.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setBrush(glow)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(
            QPointF(cx, cy),
            radius * 1.45,
            radius * 1.45,
        )

        # Dark glass sphere.
        sphere = QRadialGradient(
            QPointF(cx - radius * 0.20, cy - radius * 0.25),
            radius * 1.2,
        )
        sphere.setColorAt(0.0, QColor(44, 31, 15, 150))
        sphere.setColorAt(0.42, QColor(16, 20, 29, 205))
        sphere.setColorAt(0.82, QColor(5, 9, 16, 225))
        sphere.setColorAt(1.0, QColor(2, 5, 10, 245))
        painter.setBrush(sphere)
        painter.setPen(QPen(QColor(255, 170, 45, 110), 1.2))
        painter.drawEllipse(QPointF(cx, cy), radius, radius)

        painter.save()
        painter.translate(cx, cy)

        # Rotating latitude/longitude holographic lines.
        for i in range(12):
            a = math.radians(self.angle * (0.65 if i % 2 else -0.45) + i * 15)
            rx = radius * (0.32 + (i % 5) * 0.15)
            ry = radius * (0.92 - (i % 4) * 0.08)

            painter.save()
            painter.rotate(math.degrees(a))
            pen = QPen(QColor(255, 170, 45, 50 + (i % 3) * 18), 1)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(
                QPointF(-rx * 0.15, 0),
                rx,
                ry,
            )
            painter.restore()

        # Random orbital arcs.
        for i, (start, scale, direction, alpha) in enumerate(self.rings):
            rect_r = radius * scale
            start_deg = math.degrees(start + math.radians(self.angle * direction * 0.6))
            span = 35 + (i % 5) * 22

            pen = QPen(
                QColor(255, 185, 55, int(80 * alpha)),
                1.0 + (i % 4 == 0),
            )
            painter.setPen(pen)
            painter.drawArc(
                int(-rect_r),
                int(-rect_r),
                int(rect_r * 2),
                int(rect_r * 2),
                int(start_deg * 16),
                int(span * 16),
            )

        # Circuit-like radial traces.
        for i in range(90):
            a = math.tau * i / 90 + math.radians(self.angle * 0.18)
            inner = radius * random.Random(i + 100).uniform(0.35, 0.78)
            outer = inner + radius * random.Random(i + 200).uniform(0.015, 0.14)

            x1 = math.cos(a) * inner
            y1 = math.sin(a) * inner
            x2 = math.cos(a) * outer
            y2 = math.sin(a) * outer

            painter.setPen(QPen(QColor(255, 170, 45, 90), 1))
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

            if i % 4 == 0:
                painter.setBrush(QColor(255, 190, 55, 150))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(QPointF(x2, y2), 1.6, 1.6)

        # Dense moving holographic particles.
        for theta, r, z, brightness in self.particles:
            rot = theta + math.radians(self.angle * (0.25 + abs(z) * 0.35))
            # Compress one axis to create spherical depth.
            x = math.cos(rot) * r
            y = math.sin(rot) * r * (0.72 + 0.28 * (z + 1) / 2)

            # Keep particles around the core.
            if math.hypot(x, y) > radius * 1.12:
                continue

            depth = (z + 1) / 2
            size = 0.5 + brightness * (0.7 + depth)
            alpha = int(55 + 170 * brightness * (0.45 + depth * 0.55))

            painter.setBrush(QColor(255, 180, 45, alpha))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QPointF(x, y), size, size)

        # Central glowing core.
        core_radius = radius * (0.12 + 0.012 * math.sin(self.pulse * 1.7))
        core = QRadialGradient(QPointF(0, 0), core_radius * 2.2)
        core.setColorAt(0.0, QColor(255, 232, 155, 255))
        core.setColorAt(0.25, QColor(255, 180, 40, 220))
        core.setColorAt(0.7, QColor(255, 145, 20, 75))
        core.setColorAt(1.0, QColor(255, 120, 0, 0))
        painter.setBrush(core)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPointF(0, 0), core_radius * 2.2, core_radius * 2.2)

        painter.setBrush(QColor(255, 225, 145, 245))
        painter.drawEllipse(QPointF(0, 0), core_radius * 0.62, core_radius * 0.62)

        painter.restore()

        # Fine outer circular HUD lines.
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(255, 170, 45, 75), 1))
        painter.drawEllipse(QPointF(cx, cy), radius * 1.12, radius * 1.12)

        painter.setPen(QPen(QColor(255, 180, 50, 38), 1))
        painter.drawEllipse(QPointF(cx, cy), radius * 1.27, radius * 1.27)


class VioraWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("VIORA")
        self.resize(1100, 720)
        self.setMinimumSize(900, 620)

        self.setStyleSheet("""
            QMainWindow {
                background: #050912;
            }
            QLabel {
                color: #f6d58a;
            }
            QPushButton {
                color: #f7d99a;
                background: rgba(15, 22, 35, 210);
                border: 1px solid rgba(255, 175, 55, 110);
                border-radius: 18px;
                padding: 9px 20px;
            }
            QPushButton:hover {
                background: rgba(75, 49, 20, 220);
            }
        """)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(28, 22, 28, 24)
        layout.setSpacing(8)

        title = QLabel("VIORA")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.DemiBold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("PERSONAL INTELLIGENCE SYSTEM")
        subtitle.setFont(QFont("Segoe UI", 9))
        subtitle.setStyleSheet("color: rgba(246, 213, 138, 150); letter-spacing: 3px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status = QLabel("●  SYSTEM ONLINE")
        self.status.setFont(QFont("Segoe UI", 10))
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.core = HolographicCore()

        self.message = QLabel("Ready for your command")
        self.message.setFont(QFont("Segoe UI", 12))
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message.setStyleSheet("color: rgba(255, 220, 150, 185);")

        button = QPushButton("  🎙  ACTIVATE VIORA  ")
        button.setFixedHeight(42)
        button.setFont(QFont("Segoe UI", 10))
        button.clicked.connect(self.activate)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(4)
        layout.addWidget(self.status)
        layout.addWidget(self.core, 1)
        layout.addWidget(self.message)
        layout.addSpacing(8)
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignHCenter)

    def activate(self):
        self.status.setText("●  LISTENING")
        self.message.setText("Listening for your command...")
        QTimer.singleShot(
            1800,
            lambda: (
                self.status.setText("●  SYSTEM ONLINE"),
                self.message.setText("Ready for your command"),
            ),
        )


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("VIORA")

    window = VioraWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
