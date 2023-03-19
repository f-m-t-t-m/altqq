package org.example;

public class Main {

    public static void main(String[] args) {
        final double[][] a = {
            {0.416, 3.273, 0.326, 0.375},
            {0.297, 0.351, 2.997, 0.429},
            {0.412, 0.194, 0.215, 3.628},
            {4.003, 0.207, 0.519, 0.281}
        };
        final double[] b = {0.021, 0.213, 0.946, 0.425};
        //GaussLinearEquationSolver solver = new GaussLinearEquationSolver();
        GaussLinearEquationWithMainElementSolver solver1 = new GaussLinearEquationWithMainElementSolver();

        //double[] xs = solver.solve(a, b);
        //beautifyPrintVector(xs);

        double[] xs1 = solver1.solve(a, b);
        beautifyPrintVector(xs1);
    }

    private static void beautifyPrintVector(double[] vec) {
        for(int i = 0; i < vec.length; ++i) {
            System.out.printf("x%d = %f\n", i+1, vec[i]);
        }
    }

}