package org.example;


public class Main {

    public static void main(String[] args) {
        final double[][] a = {
                {2, -4, 4},
                {1, 1, -4},
                {3, 1, -2}
        };

        final double[] b = {36, -27, -9};

        beautifyPrintVector(OrthoSolver.solve(a, b));

    }

    private static void beautifyPrintVector(double[] vec) {
        for(int i = 0; i < vec.length; ++i) {
            System.out.printf("x%d = %f\n", i+1, vec[i]);
        }
    }

}