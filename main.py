from manim import *

background_color = "#c6b198"
nodes_color = "#4165bb"
edges_color = "#4165bb"
node_letter_color = "#c6b198"

white = "#FFFFFF"

# animatons

# animation for agreement properties
class AgreementProperties(Scene):
    def construct(self):
        self.camera.background_color = background_color

        # create text start @ center then move to top
        self.title = Text("Agreement Properties", font_size=40, color=white)
        self.play(FadeIn(self.title), run_time=1)
        self.play(self.title.animate.shift(2 * UP), run_time=1)
        self.wait(1)
                
        # properties
        properties = VGroup(
            Text("Termination", font_size=30, color=white),
            Text("Agreement", font_size=30, color=white),
            Text("Validity", font_size=30, color=white),
        )

        # animate properties
        properties.arrange(DOWN, buff=0.5)
        properties.shift(1 * DOWN)
        self.play(FadeIn(properties), run_time=1)
        self.wait(1)
        
        # move properties to top left + fadeout title
        self.play(properties.animate.shift(3 * UP + 5 * LEFT), run_time=1)
        self.play(FadeOut(self.title), run_time=1)
        self.wait(1)
        
        # graph
        graph = setupGraph()
        self.play(Create(graph), run_time=4)
        self.wait(1)

        # termination = termination text = node_color
        termination_new = Text("Termination", font_size=30, color=nodes_color)
        termination_new.move_to(properties[0])
        self.play(Transform(properties[0], termination_new), run_time=1)
        self.wait(1)

        # every process must eventually decide.
        # show each node deciding one by one
        decide_labels = {}
        checkmarks = {}
        initial_values = {"A": "1", "B": "1", "C": "0"}
        for v in ["A", "B", "C"]:
            # decision value label
            label = Text(initial_values[v], font_size=24, color=nodes_color, weight=BOLD)
            label.next_to(graph.vertices[v], RIGHT, buff=0.3)
            decide_labels[v] = label

            # checkmark
            check = Text("✓", font_size=28, color="#2e8b57", weight=BOLD)
            check.next_to(label, RIGHT, buff=0.15)
            checkmarks[v] = check

        # animate each process deciding with a brief highlight
        for v in ["A", "B", "C"]:
            self.play(
                graph.vertices[v].animate.set_stroke(WHITE, width=5),
                run_time=0.4,
            )
            self.play(
                FadeIn(decide_labels[v], shift=0.3 * RIGHT),
                FadeIn(checkmarks[v], shift=0.3 * RIGHT),
                run_time=0.6,
            )
            self.play(
                graph.vertices[v].animate.set_stroke(nodes_color, width=2),
                run_time=0.3,
            )
            self.wait(0.3)

        self.wait(1)

        # --- AGREEMENT ---
        # highlight "Agreement" in the property list
        agreement_new = Text("Agreement", font_size=30, color=nodes_color)
        agreement_new.move_to(properties[1])
        self.play(Transform(properties[1], agreement_new), run_time=1)
        self.wait(1)

        # all correct processes must decide on the same value
        # highlight all nodes simultaneously
        self.play(
            *[graph.vertices[v].animate.set_stroke(WHITE, width=5) for v in ["A", "B", "C"]],
            run_time=0.6,
        )

        # indicate all decision labels — C has "0" which doesn't match A,B's "1"
        self.play(
            *[Indicate(decide_labels[v], color=WHITE, scale_factor=1.4) for v in ["A", "B", "C"]],
            run_time=1,
        )
        self.wait(0.5)

        # highlight C's value in red to show it doesn't agree
        self.play(
            decide_labels["C"].animate.set_color("#c0392b"),
            run_time=0.5,
        )
        self.wait(0.5)

        # C receives messages from A and B (communication arrows)
        arrow_ac = Arrow(
            graph.vertices["A"].get_center(),
            graph.vertices["C"].get_center(),
            color=nodes_color,
            buff=0.6,
            stroke_width=3,
        )
        arrow_bc = Arrow(
            graph.vertices["B"].get_center(),
            graph.vertices["C"].get_center(),
            color=nodes_color,
            buff=0.6,
            stroke_width=3,
        )
        self.play(Create(arrow_ac), Create(arrow_bc), run_time=0.8)
        self.wait(0.5)

        # C changes its value from "0" to "1" (agreement reached)
        new_c_label = Text("1", font_size=24, color=nodes_color, weight=BOLD)
        new_c_label.move_to(decide_labels["C"])
        self.play(
            Transform(decide_labels["C"], new_c_label),
            FadeOut(arrow_ac),
            FadeOut(arrow_bc),
            run_time=0.8,
        )
        self.wait(0.5)

        # now all values are "1" — surround with boxes to show agreement
        agree_boxes = {}
        for v in ["A", "B", "C"]:
            box = SurroundingRectangle(
                decide_labels[v], color="#2e8b57", buff=0.08, corner_radius=0.05, stroke_width=2,
            )
            agree_boxes[v] = box

        self.play(
            *[Create(agree_boxes[v]) for v in ["A", "B", "C"]],
            run_time=0.8,
        )
        self.wait(1)

        # reset
        self.play(
            *[graph.vertices[v].animate.set_stroke(nodes_color, width=2) for v in ["A", "B", "C"]],
            *[FadeOut(agree_boxes[v]) for v in ["A", "B", "C"]],
            run_time=0.6,
        )
        self.wait(1)

        # --- VALIDITY ---
        # highlight "Validity" in the property list
        validity_new = Text("Validity", font_size=30, color=nodes_color)
        validity_new.move_to(properties[2])
        self.play(Transform(properties[2], validity_new), run_time=1)
        self.wait(1)

        # if all correct processes propose the same value, they must decide that value
        # show input values on the left of each node
        input_labels = {}
        input_checks = {}
        for v in ["A", "B", "C"]:
            label = Text("1", font_size=24, color=nodes_color, weight=BOLD)
            label.next_to(graph.vertices[v], LEFT, buff=0.3)
            input_labels[v] = label

            check = Text("✓", font_size=28, color="#2e8b57", weight=BOLD)
            check.next_to(label, LEFT, buff=0.15)
            input_checks[v] = check

        # animate each process showing input → matches output
        for v in ["A", "B", "C"]:
            self.play(
                graph.vertices[v].animate.set_stroke(WHITE, width=5),
                run_time=0.4,
            )
            self.play(
                FadeIn(input_labels[v], shift=0.3 * LEFT),
                run_time=0.6,
            )
            self.play(
                Indicate(input_labels[v], color=WHITE, scale_factor=1.3),
                Indicate(decide_labels[v], color=WHITE, scale_factor=1.3),
                run_time=0.6,
            )
            self.play(
                FadeIn(input_checks[v], shift=0.3 * LEFT),
                run_time=0.4,
            )
            self.play(
                graph.vertices[v].animate.set_stroke(nodes_color, width=2),
                run_time=0.3,
            )
            self.wait(0.3)

        self.wait(1)


def setupGraph():
    vertices = ["A", "B", "C"]
    edges = [("A", "B"), ("B", "C"), ("A", "C")]
    layout = {
        "A": 2 * UP,
        "B": 2.5 * LEFT + 1.5 * DOWN,
        "C": 2.5 * RIGHT + 1.5 * DOWN,
    }

    return Graph(
        vertices,
        edges,
        layout=layout,
        labels=True,
        vertex_config={
            "radius": 0.5, 
            "color": nodes_color,
            "fill_color": nodes_color,
            "fill_opacity": 1,
        },
        label_fill_color=node_letter_color,
        edge_config={
            "color": edges_color,
            "stroke_width": 3,
        },
    )

class Traitor(Scene):
    def construct(self):
        self.camera.background_color = background_color

        # show normal ABC graph
        graph = setupGraph()
        self.play(Create(graph), run_time=4)
        self.wait(1)

        # transform node C into the traitor (devil image)
        pos_c = graph.vertices["C"].get_center()

        devil = ImageMobject("media/images/devil.png")
        devil.set_width(1.0)
        devil.move_to(pos_c)

        # fade out the C node and fade in the devil
        self.play(
            FadeOut(graph.vertices["C"]),
            FadeIn(devil),
            run_time=1.5,
        )
        self.wait(1)