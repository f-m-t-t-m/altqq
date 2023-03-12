package org.example;

import java.util.Arrays;

public class GaussLinearEquationSolver {

    public double[] solve(double[][] a, double[] b) {
        forwardStep(a, b);
        return backwardStep(a, b);
    }

    private void forwardStep(double[][] a, double[] b) {
        int lastIndexA = a.length - 1;
        for(int i = 0; i < lastIndexA; ++i) {
            if (isMatrixTriangular(a)) {
                return;
            }
            for(int j = i + 1; j < a.length; ++j) {
                double multiplier = a[j][i]/a[i][i];
                double[] subtractLineA = copyAndMultiplyArray(a[i], multiplier);
                b[j] -= b[i]*multiplier;
                subtractLine(a[j], subtractLineA);
            }
        }
    }

    private boolean isMatrixTriangular(double[][] a) {
        for (int i = 0; i < a.length; ++i) {
            for (int j = 0; j < i; ++j) {
                if (a[i][j] != 0.0) {
                    return false;
                }
            }
        }
        return true;
    }

    private double[] copyAndMultiplyArray(double[] a, double multiplier) {
        double[] aCopy = Arrays.copyOf(a, a.length);
        for(int i = 0; i < aCopy.length; ++i) {
            aCopy[i] *= multiplier;
        }
        return aCopy;
    }

    private void subtractLine(double[] a, double[] b) {
        for(int i = 0; i < a.length; ++i) {
            a[i] -= b[i];
        }
    }

    private double[] backwardStep(double[][] a, double[] b) {
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

    public GaussLinearEquationSolver() {
    }
}
