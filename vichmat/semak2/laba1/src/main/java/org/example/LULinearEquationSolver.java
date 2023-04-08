package org.example;

import java.util.Arrays;

public class LULinearEquationSolver extends GaussLinearEquationSolver {

    @Override
    public double[] solve(double[][] a, double[] b) {
        LUDecomposition luDecomposition = new LUDecomposition(a);
        double[] Y = getY(luDecomposition.getL(), b);
        return backwardStep(luDecomposition.getU(), Y);
    }

    @Override
    public void forwardStep(double[][] a, double[] b) {
        throw new UnsupportedOperationException();
    }

    protected double[] getY(double[][] L, double[] b) {
        double[] Y = Arrays.copyOf(b, b.length);

        for (int i = 0; i < L.length; ++i) {
            for (int j = 0; j < i; ++j) {
                Y[i] -= Y[j] * L[i][j];
            }
            Y[i] /= L[i][i];
        }
        return Y;
    }

}
