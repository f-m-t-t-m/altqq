package org.example;

import java.util.Arrays;

public class MatrixUtils {

    public static boolean isMatrixTriangular(double[][] a) {
        for (int i = 0; i < a.length; ++i) {
            for (int j = 0; j < i; ++j) {
                if (Math.abs(a[i][j] - 0.0) > 10e-7d) {
                    return false;
                }
            }
        }
        return true;
    }

    public static double[] copyAndMultiplyArray(double[] a, double multiplier) {
        double[] aCopy = Arrays.copyOf(a, a.length);
        for(int i = 0; i < aCopy.length; ++i) {
            aCopy[i] *= multiplier;
        }
        return aCopy;
    }

    public static void subtractLine(double[] a, double[] b) {
        for(int i = 0; i < a.length; ++i) {
            a[i] -= b[i];
        }
    }

    public static void printMatrix(double[][] a) {
        for(double[] row: a) {
            for(double col: row) {
                System.out.printf("%f ", col);
            }
            System.out.println();
        }
        System.out.println();
    }

    private MatrixUtils() {
    }

}
