from manim import *
import random

class SemanticZippingChunksWithLogo(Scene):
    def construct(self):
        # Configuration
        rect_width = 3
        rect_height = rect_width * 1.41
        num_chunks = 5
        chunk_height = rect_height / num_chunks
        scale_factor = 0.6  # 60% of original size

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

        # Create left chunks with labels
        left_chunks = []
        for i in range(num_chunks):
            y_offset = rect_height / 2 - chunk_height / 2 - i * chunk_height
            lb = Rectangle(
                width=rect_width,
                height=chunk_height,
                fill_color=BLUE,
                fill_opacity=0.8
            ).move_to(left_rect.get_center() + UP * y_offset)
            lb_label = Text("ru", font_size=20, color=WHITE).move_to(lb.get_center())
            chunk_group = VGroup(lb, lb_label)
            left_chunks.append(chunk_group)
            self.add(chunk_group)

        self.wait(0.5)

        # Merge into center with slicing from top of right
        center_chunks = []
        current_y = rect_height / 2 - chunk_height / 2
        right_slice_top = right_rect.get_top()[1]

        for i, left_group in enumerate(left_chunks):
            # Move left chunk to next position in center stack with scaling
            self.play(
                left_group.animate.scale(scale_factor).move_to([0, current_y, 0]).set_z_index(1),
                run_time=0.5
            )
            center_chunks.append(left_group)
            current_y -= chunk_height * scale_factor

            # Simulate slicing right chunk from top with random height
            slice_height = chunk_height * random.uniform(0.5, 1.0)
            rb = Rectangle(
                width=rect_width,
                height=slice_height,
                fill_color=GREEN,
                fill_opacity=0.8
            )
            rb.move_to([right_rect.get_center()[0], right_slice_top - slice_height / 2, 0])
            right_slice_top -= slice_height

            rb_label = Text("es", font_size=20, color=WHITE).move_to(rb.get_center())
            right_group = VGroup(rb, rb_label)
            self.add(right_group)

            # Move it under the corresponding left chunk with scaling
            self.play(
                right_group.animate.scale(scale_factor).move_to([
                    0,
                    current_y - slice_height * scale_factor / 2 + chunk_height * scale_factor / 2,
                    0
                ]).set_z_index(1),
                run_time=0.5
            )
            current_y -= slice_height * scale_factor
            center_chunks.append(right_group)

        self.wait(0.5)

        # Add OpenAI logo on top
        logo = SVGMobject("openai_logo.svg")  # <-- Path to your SVG file
        logo.scale(0.7)
        logo.next_to([0, rect_height / 2, 0], UP, buff=0.3)

        self.play(FadeIn(logo, shift=UP), run_time=1)
        self.wait(1)
