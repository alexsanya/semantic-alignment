from manim import *

class SemanticZippingChunksWithLogo(Scene):
    def construct(self):
        # Configuration
        rect_width = 3
        rect_height = rect_width * 1.41
        num_chunks = 5
        chunk_height = rect_height / num_chunks

        # Rectangle shells
        left_rect = Rectangle(width=rect_width, height=rect_height).to_corner(LEFT + UP)
        right_rect = Rectangle(width=rect_width, height=rect_height).to_corner(RIGHT + UP)

        # Corner labels
        t_left = Text("T", font_size=34).next_to(left_rect.get_corner(UL), DOWN + RIGHT, buff=0.2)
        t_right = Text("T", font_size=34).next_to(right_rect.get_corner(UL), DOWN + RIGHT, buff=0.2)

        # Center language tags
        ru_label = Text("RU", font_size=30).move_to(left_rect.get_center())
        es_label = Text("ES", font_size=30).move_to(right_rect.get_center())

        self.add(left_rect, right_rect, t_left, t_right, ru_label, es_label)
        # self.play(Create(left_rect), Create(right_rect))
        # self.play(Write(t_left), Write(t_right), Write(ru_label), Write(es_label))

        # Create left and right chunks
        left_chunks = []
        right_chunks = []
        for i in range(num_chunks):
            y_offset = rect_height / 2 - chunk_height / 2 - i * chunk_height

            # Left chunk (blue)
            lb = Rectangle(
                width=rect_width,
                height=chunk_height,
                fill_color=BLUE,
                fill_opacity=0.8
            ).move_to(left_rect.get_center() + UP * y_offset)
            left_chunks.append(lb)

            # Right chunk (green)
            rb = Rectangle(
                width=rect_width,
                height=chunk_height,
                fill_color=GREEN,
                fill_opacity=0.8
            ).move_to(right_rect.get_center() + UP * y_offset)
            right_chunks.append(rb)

            self.add(lb, rb)

        self.wait(0.5)

        # Animate merging into center
        center_y_base = rect_height / 2 - chunk_height / 2
        for i in range(num_chunks):
            target_y_top = center_y_base - i * chunk_height
            target_y_bottom = -center_y_base + i * chunk_height

            self.play(
                left_chunks[i].animate.move_to([0, target_y_top, 0]).set_z_index(1),
                run_time=0.6
            )
            self.play(
                right_chunks[i].animate.move_to([0, target_y_bottom, 0]).set_z_index(1),
                run_time=0.6
            )

        self.wait(0.5)

        # Add OpenAI logo on top
        logo = SVGMobject("openAI_logo.svg")  # <-- Path to your SVG file
        logo.scale(0.7)
        logo.next_to([0, rect_height / 2, 0], UP, buff=0.3)

        self.play(FadeIn(logo, shift=UP), run_time=1)
        self.wait(1)
