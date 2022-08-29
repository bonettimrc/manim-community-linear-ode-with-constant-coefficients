from manim import *


def generateGenericPlot(f, color):
    axes = Axes(
        x_range=[-1, 7, 1],
        y_range=[-1, 7, 1],
    )
    t = ValueTracker(1)
    
    axes_labels = axes.get_axis_labels()
    generic_function = axes.plot(f, color=color)
    dot = Dot(point=[axes.c2p(t.get_value(), f(t.get_value()))])
    dot.add_updater(lambda x: x.move_to(axes.c2p(t.get_value(), f(t.get_value()))))

    plotAndLabels = VGroup(axes, generic_function, axes_labels, dot)
   
    return plotAndLabels, t
def colorizeMathTex(e):
        e.set_color_by_tex(r"k_{0}", BLUE_A)
        e.set_color_by_tex(r"k_{1}", BLUE_B)
        e.set_color_by_tex(r"k_{2}", BLUE_C)
        e.set_color_by_tex(r"k_{n}", BLUE_D)
        e.set_color_by_tex(r"y", RED_A)
        e.set_color_by_tex(r"y'", RED_B)
        e.set_color_by_tex(r"y''", RED_C)
        e.set_color_by_tex(r"y^{(n)}", RED_D)
        e.set_color_by_tex(r"\frac{dy}{dx}", RED_B)
        e.set_color_by_tex(r"\frac{d^{2}y}{dx^{2}}", RED_C)
        e.set_color_by_tex(r"\frac{d^{n}y}{dx^{n}}", RED_D)

class Introduction(Scene):
    def construct(self):
        title=Tex(r"Linear Ordinal Differential Equations\\with ",r"Constant", r" Coefficients", font_size=70)
        title.set_color_by_tex(r"Constant", BLUE)
        subtitle=Tex(r"Introduction")
        self.play(Create(title))
        self.wait(2)
        self.play(ReplacementTransform(title,subtitle))
        self.wait(2)
        self.play(FadeOut(subtitle, shift=UP*4))
        e1 =  MathTex(r"k_{0}",r"y",r"+",r"k_{1}",r"y'",r"+",r"k_{2}",r"y''",r"+",r"\cdots",r"+",r"k_{n}",r"y^{(n)}",r"=",r"0")
        colorizeMathTex(e1)
        self.play(Create(e1))
        self.wait(2)
        # move the equation to make space for the plots
        self.play(e1.animate.to_edge(UP))        
        # adds a plot to help visualize constants
        constantPlot, constantTracker = generateGenericPlot(lambda x:4, BLUE)
        constantPlot.scale(0.5)
        constantPlot.to_edge(DOWN,buff=1)
        # the constants all shifts to a generic constant to represent them all
        k_i=MathTex(r"k_{i}")
        k_i.set_color(BLUE)
        k_i.scale(1.2)
        k_i.next_to(constantPlot, UP, buff=1)
        ks = e1.get_parts_by_tex(r"k")
        self.play(TransformFromCopy(ks,k_i))
        self.play(Create(constantPlot))
        self.play(constantTracker.animate.set_value(5))
        self.play(constantTracker.animate.set_value(2))
        self.play(constantTracker.animate.set_value(6))
        self.wait(2)
        
        # adds a plot to help visualize variables
        functionPlot, functionTracker = generateGenericPlot(lambda x:0.9*np.sin(0.75*x+1)+4, RED_A)
        functionPlot.scale(0.5)
        functionPlot.to_edge(DOWN,buff=1)
        # the function is focused
        xMapsToY=MathTex(r"x\mapsto y")
        xMapsToY.set_color(RED_A)
        xMapsToY.scale(1.2)
        xMapsToY.next_to(functionPlot, UP, buff=1)
        y = e1.get_part_by_tex(r"y")
        self.play(Uncreate(k_i), TransformFromCopy(y,xMapsToY))
        self.play(ReplacementTransform(constantPlot,functionPlot))
        self.play(functionTracker.animate.set_value(5))
        self.play(functionTracker.animate.set_value(2))
        self.play(functionTracker.animate.set_value(6))
        self.play(functionTracker.animate.set_value(1))
        self.wait(2)
        # adds a plot to help visualize the first derivative
        derivativePlot, derivativeTracker = generateGenericPlot(lambda x:0.75*0.9*np.cos(0.75*x+1), RED_B)
        derivativePlot.scale(0.5)
        derivativePlot.to_edge(DOWN, buff=1)
        derivativePlot.next_to(functionPlot, RIGHT, buff=1)
        # the first derivative is focused
        xMapsToDerivativeOfY=MathTex(r"x\mapsto y'")
        xMapsToDerivativeOfY.set_color(RED_B)
        xMapsToDerivativeOfY.scale(1.2)
        xMapsToDerivativeOfY.next_to(derivativePlot, UP, buff=1)
        derivativeOfY = e1.get_part_by_tex(r"y'")
        vgroup1 = VGroup(xMapsToY,xMapsToDerivativeOfY)
        vgroup2 = VGroup(functionPlot,derivativePlot)
        self.play(vgroup2.animate.move_to(ORIGIN).to_edge(DOWN,buff=1))
        self.play(vgroup1.animate.move_to(ORIGIN).next_to(vgroup2, UP, buff=1), )
        self.play(TransformFromCopy(derivativeOfY,xMapsToDerivativeOfY))
        self.play(Create(derivativePlot))
        tangentLine = TangentLine(functionPlot[1], (functionTracker.get_value()+1)/8, length=2, color=GREEN)
        # why? why was it so difficult to notice that alpha must be between 0 and 1? it took me 2 hours to understant why it wasn't working
        tangentLine.add_updater(lambda mob: mob.become(TangentLine(functionPlot[1], (functionTracker.get_value()+1)/8, length=2, color=GREEN)))
        
        self.play(Create(tangentLine))
        self.play(derivativeTracker.animate.set_value(5),functionTracker.animate.set_value(5))
        self.play(derivativeTracker.animate.set_value(2),functionTracker.animate.set_value(2))
        self.play(derivativeTracker.animate.set_value(6),functionTracker.animate.set_value(6))
        self.wait(2)
        self.play(Uncreate(vgroup1),Uncreate(vgroup2),e1.animate.move_to(ORIGIN))
        self.wait(2)
        lagrange=ImageMobject("./lagrange.jpg")
        lagrange.scale_to_fit_width(3)
        self.play(e1.animate.scale(0.8))
        lagrange.next_to(e1, LEFT)
        self.play(FadeIn(lagrange))
        self.wait(2)
        euler=ImageMobject("./euler.jpg")
        euler.scale_to_fit_width(3)
        euler.next_to(e1,RIGHT)
        self.play(FadeIn(euler))
        self.wait(2)
        self.play(FadeOut(lagrange), FadeOut(euler), e1.animate.scale(1.25))
        self.wait(2)
        leibniz=ImageMobject("./leibniz.jpg")
        leibniz.scale_to_fit_width(3)
        # e2 is e1 but in leibniz notation
        e2 =MathTex(r"k_{0}",r"y",r"+",r"k_{1}",r"\frac{dy}{dx}",r"+",r"k_{2}",r"\frac{d^{2}y}{dx^{2}}",r"+",r"\cdots",r"+",r"k_{n}",r"\frac{d^{n}y}{dx^{n}}",r"=",r"0")
        # sets the same color scheme as e1's
        colorizeMathTex(e2)
        # e1 becomes e2
        
        self.play(TransformMatchingTex(e1, e2))
        self.wait(2)
        self.play(e2.animate.to_edge(RIGHT).shift(LEFT*0.5))
        leibniz.next_to(e2,LEFT,buff=1)
        self.play(FadeIn(leibniz))
        self.wait(2)
class FirstOrderOrdinalDifferentialEquationswithConstantCoefficients(Scene):
    def construct(self):
        class Step():
            def __init__(self, equation, f=None):
                self.equation = equation
                self.f = f
        def f1(scene, mathTex: MathTex):
            cross1 = Cross(mathTex.get_parts_by_tex(r"y")[2])
            cross2 = Cross(mathTex.get_parts_by_tex(r"y")[3])
            scene.play(Create(cross1), Create(cross2))
            scene.play(Uncreate(mathTex.get_parts_by_tex(r"y")[2]), Uncreate(VGroup(mathTex[-1], mathTex[-2], mathTex[-3])),Uncreate(cross1), Uncreate(cross2))
        def f2(scene, mathTex: MathTex):
            firstInstance = mathTex.get_parts_by_tex(r"k_{1}")[0]
            secondInstance = mathTex.get_parts_by_tex(r"k_{1}")[1]
            secondInstanceDelete = VGroup(mathTex[0], mathTex[1], mathTex[2])
            cross1 = Cross(firstInstance)
            cross2 = Cross(secondInstance)
            scene.play(Create(cross1), Create(cross2))
            scene.play(Uncreate(firstInstance), Uncreate(secondInstanceDelete),Uncreate(cross1), Uncreate(cross2))
        def f3(scene, mathTex: MathTex):
            firstInstance = mathTex.get_parts_by_tex(r"e")[0]
            secondInstance = mathTex.get_parts_by_tex(r"\ln")[0]
            secondInstanceDelete = secondInstance
            cross1 = Cross(firstInstance)
            cross2 = Cross(secondInstance)
            scene.play(Create(cross1), Create(cross2))
            scene.play(Uncreate(firstInstance), Uncreate(secondInstanceDelete),Uncreate(cross1), Uncreate(cross2))
        steps = [
            Step(r"k_{0};y;+;k_{1};y';+;k_{2};y'';+;\cdots;+;k_{n};y^{(n)};=;0"                    ),#
            Step(r"k_{0};y;+;k_{1};\frac{dy}{dx};=;0"                                              ),#
            Step(r"-k_{0};y;+;k_{0};y;+;k_{1};\frac{dy}{dx};=;0;-k_{0};y"                          ),#
            Step(r"k_{1};\frac{dy}{dx};=;-k_{0};y",                                                ),#
            Step(r"{1;\over; y};k_{1};\frac{dy}{dx};=;-k_{0};y;{1;\over; y}",f1                    ),#
            Step(r"{k_{1};\over; y};\frac{dy}{dx};=;-k_{0}"                                        ),#
            Step(r"{1;\over; k_{1}};{k_{1};\over; y};\frac{dy}{dx};=;-k_{0};{1;\over; k_{1}}", f2  ),#
            Step(r"{1;\over; y};\frac{dy}{dx};=;-k_{0};{1;\over; k_{1}}"                           ),#
            Step(r"{1;\over; y};\frac{dy}{dx};=;-;{k_{0};\over; k_{1}}"                            ),#
            Step(r"\int;{1;\over; y};\frac{dy}{dx};dx;=;\int;-;{k_{0};\over; k_{1}};dx"            ),#
            Step(r"\int;{1;\over; y};dy;=;-;{k_{0};\over; k_{1}};\int; dx"                         ),#
            Step(r"\ln|;y;|;+;C_{1};=;-;{k_{0};\over; k_{1}};x;+;C_{2}"                            ),#
            Step(r"\ln|;y;|;=;-;{k_{0};\over; k_{1}};x;+;C",                                       ),#
            Step(r"e;^{;\ln;|;y;|};=;e^{;-;{k_{0};\over; k_{1}};x;+;C}",f3                         ),#
            Step(r"|;y;|;=;e^{;-;{k_{0};\over; k_{1}};x};e^{;C;}"                                  ),#
            Step(r"|;y;|;=;C;e^{;-;{k_{0};\over; k_{1}};x}"                                        ),#
        ]

        lastMathTex = None
        lastF = None
        for step in steps:
            mathTex = MathTex(*step.equation.split(";"))
            if(lastF):
                lastF(self, lastMathTex)
            colorizeMathTex(mathTex)
            if(lastMathTex):
                self.play(Transform(lastMathTex,mathTex), run_time=10)
            else:
                self.play(Create(mathTex))
            if(step.f):
                lastF = step.f
            else:
                lastF = None
            lastMathTex = mathTex
            self.wait(2)
