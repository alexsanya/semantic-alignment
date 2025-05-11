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
        t_left = Text("T", font_size=24).next_to(left_rect.get_corner(UL), DOWN + RIGHT, buff=0.2)
        t_right = Text("T", font_size=24).next_to(right_rect.get_corner(UL), DOWN + RIGHT, buff=0.2)

        # Center language tags
        ru_label = Text("RU", font_size=30).move_to(left_rect.get_center())
        es_label = Text("ES", font_size=30).move_to(right_rect.get_center())

        # Instantly add elements to the scene
        self.add(left_rect, right_rect, t_left, t_right, ru_label, es_label)

        # Create left and right chunks with labels
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
            lb_label = Text("ru", font_size=20, color=WHITE).move_to(lb.get_center())
            left_chunks.append(VGroup(lb, lb_label))

            # Right chunk (green)
            rb = Rectangle(
                width=rect_width,
                height=chunk_height,
                fill_color=GREEN,
                fill_opacity=0.8
            ).move_to(right_rect.get_center() + UP * y_offset)
            rb_label = Text("es", font_size=20, color=WHITE).move_to(rb.get_center())
            right_chunks.append(VGroup(rb, rb_label))

            self.add(lb, lb_label, rb, rb_label)

        self.wait(0.5)

        # Alternating stack of chunks from top to bottom
        center_chunks = []
        for i in range(num_chunks):
            center_chunks.append(left_chunks[i])
            center_chunks.append(right_chunks[i])

        for i, chunk_group in enumerate(center_chunks):
            target_y = rect_height / 2 - chunk_height / 2 - i * chunk_height
            self.play(chunk_group.animate.move_to([0, target_y, 0]).set_z_index(1), run_time=0.5)

        self.wait(0.5)

        # Add OpenAI logo on top
        logo = SVGMobject("openai_logo.svg")  # <-- Path to your SVG file
        logo.scale(0.7)
        logo.next_to([0, rect_height / 2, 0], UP, buff=0.3)

        self.play(FadeIn(logo, shift=UP), run_time=1)
        self.wait(1)
