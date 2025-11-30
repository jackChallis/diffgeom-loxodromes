from manim import *
import numpy as np

class LoxodromeAutumn(ThreeDScene):
    def construct(self):
        # 1. Camera Setup
        self.camera.background_color = "#1a1a1a"  # Dark Grey background for contrast
        # Set camera to look slightly down at the sphere
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        # 2. Design Parameters
        R = 2.5                 # Radius of sphere
        NUM_RIBBONS = 12        # Total number of strips to cover the sphere
        TURNS = 2               # How many times the spiral winds around

        # The "Autumn" Palette from the image
        # Navy, Mustard, Maroon, Olive
        PALETTE = ["#1f3b75", "#d69836", "#a33232", "#6b8e23"]

        # 3. Helper Function: Loxodrome Math
        def get_loxodrome_func(index):
            # Calculate the offset for this specific ribbon
            angle_offset = (index / NUM_RIBBONS) * TAU

            # The curve function
            def func(t):
                # t is latitude (phi), from -PI/2 to PI/2
                # We clamp it slightly to avoid infinite log values at exact poles
                phi = t

                # Math for Rhumb line longitude: lambda = constant * ln(tan(phi/2 + pi/4))
                # The 'constant' controls the steepness/number of turns
                # We scale it so it wraps 'TURNS' times over the latitude range
                scaling_factor = TURNS / np.pi
                lam = scaling_factor * np.log(np.tan(phi / 2 + np.pi / 4)) + angle_offset

                # Spherical to Cartesian
                x = R * np.cos(phi) * np.cos(lam)
                y = R * np.cos(phi) * np.sin(lam)
                z = R * np.sin(phi)

                return np.array([x, y, z])
            return func

        # 4. Create the Geometry
        ribbons = VGroup()

        # Create curves
        for i in range(NUM_RIBBONS):
            color = PALETTE[i % len(PALETTE)]

            # Range: almost -PI/2 to almost PI/2
            curve = ParametricFunction(
                get_loxodrome_func(i),
                t_range=[-1.5, 1.5],  # 1.57 is pi/2, so 1.5 stops just short of pole
                dt=0.01,
                stroke_width=20,      # Thick lines to simulate ribbons
                stroke_color=color
            )
            ribbons.add(curve)

        # 5. Animation Sequence

        # Animation A: Draw the ribbons spiraling up
        self.play(
            LaggedStart(
                *[Create(ribbon) for ribbon in ribbons],
                lag_ratio=0.1
            ),
            run_time=4,
            rate_func=smooth
        )

        # Animation B: Continuous Rotation
        # We rotate the group about the Z-axis
        self.begin_ambient_camera_rotation(rate=0.4)

        # Optional: Pulse the scale slightly to make it feel alive
        self.play(
            ribbons.animate.scale(1.1),
            run_time=2,
            rate_func=there_and_back
        )

        self.wait(3)
