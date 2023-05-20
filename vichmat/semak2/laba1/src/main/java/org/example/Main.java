package org.example;

public class Main {

    public static void main(String[] args) {
        final double[][] a = {
                {5, 1, 3},
                {3, 6, 3},
                {0, 2, 3}};
        final double[] b = {3, 4, 5};

        System.out.println("-------------------------------------------------------------------------");
        beautifyPrintVector(new SimpleIteration().solve(a, b));
        System.out.println("-------------------------------------------------------------------------");
        beautifyPrintVector(new SeidelMethod().solve(a, b));
        System.out.println("-------------------------------------------------------------------------");
        beautifyPrintVector(new RelaxMethod().solve(a, b));
        System.out.println("-------------------------------------------------------------------------");
    }

    private static void beautifyPrintVector(double[] vec) {
        for(int i = 0; i < vec.length; ++i) {
            System.out.printf("x%d = %.6f\n", i+1, vec[i]);
        }
    }
}