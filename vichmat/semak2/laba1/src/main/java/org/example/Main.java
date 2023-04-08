package org.example;

public class Main {

    public static void main(String[] args) {
        final double[][] a = {
                {4, 1, 1, 5},
                {1, 5, 3, 15},
                {1, 3, 15, 6},
                {5, 15, 6, 50}
        };
        final double[] b = {10, 12, 8, 7};
        CholeskyLinearEquationSolver solver = new CholeskyLinearEquationSolver();
        double[] x = solver.solve(a, b);
        beautifyPrintVector(x);
    }

    private static void beautifyPrintVector(double[] vec) {
        for(int i = 0; i < vec.length; ++i) {
            System.out.printf("x%d = %f\n", i+1, vec[i]);
        }
    }

}