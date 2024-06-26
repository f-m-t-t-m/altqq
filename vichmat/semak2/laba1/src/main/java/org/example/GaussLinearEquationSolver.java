package org.example;

import java.util.Arrays;

import static org.example.MatrixUtils.*;

public class GaussLinearEquationSolver {

    public double[] solve(double[][] a, double[] b) {
        if (a.length != a[0].length) {
            throw new IllegalArgumentException("Матрица A не является квадратной");
        }
        double[][] f = new double[a.length][];
        for (int i = 0; i < a.length; ++i) {
            f[i] = Arrays.copyOf(a[i], a[i].length);
        }
        double[] s = Arrays.copyOf(b, b.length);

        forwardStep(f, s);
        return backwardStep(f, s);
    }

    public void forwardStep(double[][] a, double[] b) {
        int lastIndexA = a.length - 1;
        for(int i = 0; i < lastIndexA; ++i) {
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

    public double[] backwardStep(double[][] a, double[] b) {
        double[] ans = Arrays.copyOf(b, b.length);
        int lastIndexA = a.length - 1;
        for(int i = lastIndexA; i >= 0; --i) {
            for(int j = i + 1; j < b.length; ++j) {
                ans[i] -= ans[j]*a[i][j];
            }
            ans[i] /= a[i][i];
        }
        return ans;
    }
}
