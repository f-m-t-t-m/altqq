package org.example;

import java.util.Arrays;

import static org.example.MatrixUtils.*;

public class GaussLinearEquationSolverPivot extends GaussLinearEquationSolver {

    public static class Point {
        private final int x;
        private final int y;

        public int getX() {
            return x;
        }

        public int getY() {
            return y;
        }

        public Point(int x, int y) {
            this.x = x;
            this.y = y;
        }
    }

    @Override
    public double[] solve(double[][] a, double[] b) {
        if (a.length != a[0].length) {
            throw new IllegalArgumentException("Матрица A не является квадратной");
        }
        double[][] f = new double[a.length][];
        for (int i = 0; i < a.length; ++i) {
            f[i] = Arrays.copyOf(a[i], a[i].length);
        }
        double[] s = Arrays.copyOf(b, b.length);
        int[] ansConsequence = new int[a[0].length];
        for (int i = 0; i < ansConsequence.length; ++i) {
            ansConsequence[i] = i;
        }
        forwardStep(f, s, ansConsequence);
        return backwardStep(f, s, ansConsequence);
    }

    public void forwardStep(double[][] a, double[] b, int[] ansConsequence) {
        int lastIndexA = a.length - 1;
        for(int i = 0; i < lastIndexA; ++i) {
            Point max = findPivot(a, i, i);
            swapRows(a, b, max.getX(), i);
            swapCols(a, max.getY(), i, ansConsequence);
            if (a[i][i] == 0) {
                throw new ArithmeticException(String.format("В результате преобразований на " +
                        "%d строке диагональный элемент равен 0", i+1));
            }
            for(int j = i + 1; j < a.length; ++j) {
                double multiplier = a[j][i]/a[i][i];
                double[] subtractLineA = copyAndMultiplyArray(a[i], multiplier);
                b[j] -= b[i]*multiplier;
                subtractLine(a[j], subtractLineA);
            }
        }
        if (a[lastIndexA][lastIndexA] == 0) {
            throw new ArithmeticException(String.format("В результате преобразований на " +
                    "%d строке диагональный элемент равен 0", lastIndexA+1));
        }
    }

    public double[] backwardStep(double[][] a, double[] b, int[] ansConsequence) {
        double[] ans =  super.backwardStep(a, b);
        return buildAnswer(ans, ansConsequence);
    }

    double[] buildAnswer(double[] ans, int[] ansConsequence) {
        double[] res = new double[ans.length];
        for (int i = 0; i < ans.length; ++i) {
            res[ansConsequence[i]] = ans[i];
        }
        return res;
    }

    public Point findPivot(double[][] a, int rowNumber, int colNumber) {
        int colOfMax = colNumber;
        int rowOfMax = rowNumber;
        for (int i = rowNumber; i < a.length; ++i) {
            for (int j = colNumber; j < a[0].length; ++j) {
                if (Math.abs(a[i][j]) > Math.abs(a[rowOfMax][colOfMax])) {
                    rowOfMax = i;
                    colOfMax = j;
                }
            }
        }
        return new Point(rowOfMax, colOfMax);
    }

    private void swapRows(double[][] a, double[] b, int from, int to) {
        double[] tmpA = a[to];
        a[to] = a[from];
        a[from] = tmpA;

        double tmpB = b[to];
        b[to] = b[from];
        b[from] = tmpB;
    }

    private void swapCols(double[][] a, int from, int to, int[] ansConsequence) {
        for (int i = 0; i < a.length; i++) {
            double tmp = a[i][to];
            a[i][to] = a[i][from];
            a[i][from] = tmp;
        }
        int tmpAns = ansConsequence[to];
        ansConsequence[to] = ansConsequence[from];
        ansConsequence[from] = tmpAns;
    }

}
