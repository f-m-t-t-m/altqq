package org.example;

import java.util.Arrays;

import static org.example.MatrixUtils.*;

public class GaussLinearEquationSolver {

    public double[] solve(double[][] a, double[] b) {
        forwardStep(a, b);
        return backwardStep(a, b);
    }

    protected void forwardStep(double[][] a, double[] b) {
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

    protected double[] backwardStep(double[][] a, double[] b) {
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
