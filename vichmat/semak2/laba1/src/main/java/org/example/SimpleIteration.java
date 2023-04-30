package org.example;

import static org.example.MatrixUtils.*;
public class SimpleIteration {

    public static double[] solve(double[][] a, double[] b) {
        double[][] solveMatrix = buildSolveMatrix(a);
        double[] curX = {1, -5, 2};
        double[] prevX;
        do {
            prevX = curX;
            curX = calcNewX(a, b, prevX, solveMatrix);
        } while (Math.abs(max(prevX) - max(curX)) > 1e-6);

        return curX;
    }

    private static double[][] buildSolveMatrix(double[][] a) {
        double[][] solveMatrix = new double[a.length][a[0].length];
        for (int i = 0; i < a.length; ++i) {
            for (int j = 0; j < a[i].length; ++j) {
                if (i == j) {
                    continue;
                }
                solveMatrix[i][j] = -a[i][j];
            }
        }
        return solveMatrix;
    }

    private static double[] calcNewX(double[][] a, double[] b, double[] oldX, double[][] solveMatrix) {
        double[] newX = new double[b.length];
        for (int i = 0; i < a.length; ++i) {
            for (int j = 0; j < b.length; ++j) {
                newX[i] += solveMatrix[i][j] * oldX[j];
            }
            newX[i] += b[i];
            newX[i] /= a[i][i];
        }
        return newX;
    }

}
