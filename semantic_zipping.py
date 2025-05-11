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

        # Create left chunks without labels initially
        left_chunks = []
        left_labels = []
        for i in range(num_chunks):
            y_offset = rect_height / 2 - chunk_height / 2 - i * chunk_height
            lb = Rectangle(
                width=rect_width,
                height=chunk_height,
                fill_color=BLUE,
                fill_opacity=0.8
            ).move_to(left_rect.get_center() + UP * y_offset).set_z_index(2)
            lb_label = Text("ru", font_size=20, color=BLACK)
            lb_label.set_z_index(2)
            left_chunks.append(lb)
            left_labels.append(lb_label)
            self.add(lb)

        self.wait(0.5)

        # Merge into center with slicing from top of right
        center_chunks = []
        current_y = rect_height / 2 - chunk_height / 2
        right_slice_top = right_rect.get_top()[1]

        for i, lb in enumerate(left_chunks):
            # Move left chunk to next position in center stack with scaling
            self.play(
                lb.animate.scale(scale_factor).move_to([0, current_y, 0]).set_z_index(1),
                run_time=0.5
            )
            lb_label = left_labels[i].move_to(lb.get_center())
            self.add(lb_label)
            center_chunks.append(VGroup(lb, lb_label))
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

            rb_label = Text("es", font_size=20, color=BLACK)
            self.add(rb)

            # Move it under the corresponding left chunk with scaling
            self.play(
                rb.animate.scale(scale_factor).move_to([
                    0,
                    current_y - slice_height * scale_factor / 2 + chunk_height * scale_factor / 2,
                    0
                ]).set_z_index(1),
                run_time=0.5
            )
            rb_label.move_to(rb.get_center()).set_z_index(2)
            self.add(rb_label)
            current_y -= slice_height * scale_factor
            center_chunks.append(VGroup(rb, rb_label))

        self.wait(0.5)

        # Add OpenAI logo on top
        logo = SVGMobject("openai_logo.svg")  # <-- Path to your SVG file
        logo.scale(0.7)
        logo.next_to([0, rect_height / 2, 0], UP, buff=0.3)

        self.play(FadeIn(logo, shift=UP), run_time=1)
        self.wait(1)
