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
        self.graph = setupGraph()
        self.play(Create(self.graph), run_time=4)

        # shift left
        self.play(self.graph.animate.shift(2 * LEFT), run_time=1)

        # node values
        self.node_vals = {'A' : 1, 'B' : 0, 'C' : 1}

        # show node values
        label = {}
        for v in self.node_vals:
            label[v] = Text(str(self.node_vals[v]), font_size=24, color=nodes_color)
            label[v].next_to(self.graph.vertices[v], buff=0.3, direction=DOWN)
            self.add(label[v])

        # initialize inbox display (each node starts with its own value)
        inbox = {}
        inbox_text = {}
        inbox_text_group = VGroup()
        shift = 2.5
        for v in self.node_vals:
            inbox[v] = [str(self.node_vals[v])]
            inbox_text[v] = Text(f"{v} = [{self.node_vals[v]}]", font_size=20, color=nodes_color)
            inbox_text[v].next_to(self.graph, buff=0.3, direction=RIGHT)
            inbox_text_group.add(inbox_text[v])
        inbox_text_group.arrange(DOWN, aligned_edge=LEFT)
        inbox_text_group.shift(shift * RIGHT)
        self.play(FadeIn(inbox_text_group), run_time=0.3)

        # send values and update inboxes after each send
        for v in self.node_vals:
            others = [d for d in self.node_vals if d != v]
            msg, dest_pos = self.sendMessage(v, others, color=white)
            for d in dest_pos:
                inbox[d].append(str(self.node_vals[v]))
                # animate message flying from dest node into the inbox text
                new_text = Text(f"{d} = [{', '.join(inbox[d])}]", font_size=20, color=nodes_color)
                new_text.move_to(inbox_text[d])
                self.play(
                    msg[d].animate.move_to(inbox_text[d].get_center()),
                    run_time=0.5,
                )
                self.play(
                    FadeOut(msg[d]),
                    Transform(inbox_text[d], new_text),
                    run_time=0.4,
                )

        self.wait(1)
        
        # display decision of each node
        decision_A = Text("= 1", font_size=20, color=nodes_color)
        decision_A.next_to(inbox_text["A"], buff=0.3, direction=RIGHT)
        self.play(Write(decision_A), run_time=1)

        decision_B = Text("= 1", font_size=20, color=nodes_color)
        decision_B.next_to(inbox_text["B"], buff=0.3, direction=RIGHT)
        self.play(Write(decision_B), run_time=1)

        decision_C = Text("= 1", font_size=20, color=nodes_color)
        decision_C.next_to(inbox_text["C"], buff=0.3, direction=RIGHT)
        self.play(Write(decision_C), run_time=1)
            
        self.wait(1)

        # fadeout inboxes and value labels
        self.play(FadeOut(inbox_text_group), run_time=0.3)
        self.play(FadeOut(decision_A), FadeOut(decision_B), FadeOut(decision_C), run_time=0.3)
        self.play(*[FadeOut(label[v]) for v in label], run_time=0.3)
        self.wait(1)

        # ----------TRAITOR-----------
        # transform node C into the traitor (devil image)
        pos_c = self.graph.vertices["C"].get_center()

        devil = ImageMobject("media/images/devil.png")
        devil.set_width(1.5)
        devil.move_to(pos_c)

        # build new edges that stop at the devil's border
        edge_ac = Line(
            self.graph.vertices["A"].get_center(),
            devil.get_center(),
            color=edges_color,
            stroke_width=3,
        ).set_length(
            Line(self.graph.vertices["A"].get_center(), devil.get_center()).get_length()
            - 0.5 - devil.get_width() / 2
        )
        edge_ac.move_to((self.graph.vertices["A"].get_center() + devil.get_center()) / 2)

        edge_bc = Line(
            self.graph.vertices["B"].get_center(),
            devil.get_center(),
            color=edges_color,
            stroke_width=3,
        ).set_length(
            Line(self.graph.vertices["B"].get_center(), devil.get_center()).get_length()
            - 0.5 - devil.get_width() / 2
        )
        edge_bc.move_to((self.graph.vertices["B"].get_center() + devil.get_center()) / 2)

        # fade out C node + old edges, fade in devil + new edges
        self.play(
            FadeOut(self.graph.vertices["C"]),
            FadeOut(self.graph.edges[("A", "C")]),
            FadeOut(self.graph.edges[("B", "C")]),
            FadeIn(devil),
            FadeIn(edge_ac),
            FadeIn(edge_bc),
            run_time=1.5,
        )
        self.wait(1)

        # --- traitor message passing (same animation, conflicting values) ---
        # initialize inboxes for A and B only
        t_inbox = {}
        t_inbox_text = {}
        t_inbox_group = VGroup()
        label = {}
        for v in ["A", "B"]:
            label[v] = Text(str(self.node_vals[v]), font_size=24, color=nodes_color)
            label[v].next_to(self.graph.vertices[v], buff=0.3, direction=DOWN)
            self.add(label[v])
            t_inbox[v] = [str(self.node_vals[v])]
            t_inbox_text[v] = Text(f"{v} = [{self.node_vals[v]}]", font_size=20, color=nodes_color)
            t_inbox_text[v].next_to(self.graph, buff=0.3, direction=RIGHT)
            t_inbox_group.add(t_inbox_text[v])
        traitor_label = Text("?", font_size=24, color=nodes_color)
        traitor_label.next_to(devil, buff=0.3, direction=DOWN)
        self.add(traitor_label)
        t_inbox_group.arrange(DOWN, aligned_edge=LEFT)
        t_inbox_group.shift(2.5 * RIGHT)
        self.play(FadeIn(t_inbox_group), run_time=0.3)

        # A sends its value to B (and to C, but we ignore C's inbox)
        for sender in ["A", "B"]:
            receiver = "B" if sender == "A" else "A"
            val = str(self.node_vals[sender])
            # send to both the other honest node and the devil
            msg_honest = Text(val, font_size=24, color=white)
            msg_honest.move_to(self.graph.vertices[sender].get_center())
            msg_devil = Text(val, font_size=24, color=white)
            msg_devil.move_to(self.graph.vertices[sender].get_center())
            self.play(FadeIn(msg_honest), FadeIn(msg_devil), run_time=0.5)
            self.play(
                msg_honest.animate.move_to(self.graph.vertices[receiver].get_center()),
                msg_devil.animate.move_to(devil.get_center()),
                run_time=1,
            )
            self.play(FadeOut(msg_devil), run_time=0.3)
            # update honest receiver's inbox
            t_inbox[receiver].append(val)
            new_text = Text(f"{receiver} = [{', '.join(t_inbox[receiver])}]", font_size=20, color=nodes_color)
            new_text.move_to(t_inbox_text[receiver])
            self.play(
                msg_honest.animate.move_to(t_inbox_text[receiver].get_center()),
                run_time=0.5,
            )
            self.play(
                FadeOut(msg_honest),
                Transform(t_inbox_text[receiver], new_text),
                run_time=0.4,
            )

        # C (traitor) sends 1 to A and 0 to B
        msg_to_a = Text("1", font_size=24, color=white)
        msg_to_a.move_to(devil.get_center())
        msg_to_b = Text("0", font_size=24, color=white)
        msg_to_b.move_to(devil.get_center())
        self.play(FadeIn(msg_to_a), FadeIn(msg_to_b), run_time=0.5)
        self.play(
            msg_to_a.animate.move_to(self.graph.vertices["A"].get_center()),
            msg_to_b.animate.move_to(self.graph.vertices["B"].get_center()),
            run_time=1,
        )
        self.wait(0.5)

        # update A's inbox with "1" from traitor
        t_inbox["A"].append("1")
        new_a = Text(f"A = [{', '.join(t_inbox['A'])}]", font_size=20, color=nodes_color)
        new_a.move_to(t_inbox_text["A"])
        self.play(
            msg_to_a.animate.move_to(t_inbox_text["A"].get_center()),
            run_time=0.5,
        )
        self.play(
            FadeOut(msg_to_a),
            Transform(t_inbox_text["A"], new_a),
            run_time=0.4,
        )

        # update B's inbox with "0" from traitor
        t_inbox["B"].append("0")
        new_b = Text(f"B = [{', '.join(t_inbox['B'])}]", font_size=20, color=nodes_color)
        new_b.move_to(t_inbox_text["B"])
        self.play(
            msg_to_b.animate.move_to(t_inbox_text["B"].get_center()),
            run_time=0.5,
        )
        self.play(
            FadeOut(msg_to_b),
            Transform(t_inbox_text["B"], new_b),
            run_time=0.4,
        )
        self.wait(1)

        # A decides 1 (majority of [1, 0, 1]), B decides 0 (majority of [0, 1, 0])
        t_decision_A = Text("= 1", font_size=20, color=nodes_color)
        t_decision_A.next_to(t_inbox_text["A"], buff=0.3, direction=RIGHT)
        self.play(Write(t_decision_A), run_time=1)

        t_decision_B = Text("= 0", font_size=20, color=nodes_color)
        t_decision_B.next_to(t_inbox_text["B"], buff=0.3, direction=RIGHT)
        self.play(Write(t_decision_B), run_time=1)

        self.wait(1)

        # fadeout
        self.play(FadeOut(t_inbox_group), run_time=0.3)
        self.play(FadeOut(t_decision_A), FadeOut(t_decision_B), run_time=0.3)
        self.wait(1)
            


    def sendMessage(self, source, dest: list, color=white):
        source_pos = self.graph.vertices[source].get_center()

        # build message objects keyed by destination
        msg = {}
        dest_pos = {}
        for d in dest:
            dest_pos[d] = self.graph.vertices[d].get_center()
            val_str = str(self.node_vals[source])
            msg[d] = Text(val_str, font_size=24, color=color)
            msg[d].move_to(source_pos)

        # fade in all messages at source
        self.play(*[FadeIn(msg[d]) for d in dest], run_time=0.5)

        # animate all messages moving to their destinations
        self.play(*[msg[d].animate.move_to(dest_pos[d]) for d in dest], run_time=1)
        self.wait(1)

        # return messages still on screen so caller can animate them into inbox
        return msg, dest_pos


        