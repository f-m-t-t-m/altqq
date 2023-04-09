package org.example;


import static org.example.MatrixUtils.*;

public class OrthoSolver {

    public static double[] solve(double[][] a, double[] b) {
        double[][] union = unionMatrices(a, b);

        double[][] v = new double[union.length][union.length];
        double[] u = union[0].clone();

        v[0] = divide(u, norm(u));
        for (int i = 1; i < union.length; ++i) {
            u = minus(union[i], calculateSum(i, union, v));
            v[i] = divide(u, norm(u));
        }
        double[] ans = new double[b.length];
        for (int i = 0; i < ans.length; ++i) {
            ans[i] = v[v.length-1][i] / v[v.length-1][v.length-1];
        }
        return ans;
    }

    private static double[][] unionMatrices(double[][] a, double[] b) {
        double[][] union = new double[b.length+1][b.length+1];
        for (int i = 0; i < a.length; i++) {
            System.arraycopy(a[i], 0, union[i], 0, a.length);
        }
        for (int i = 0; i < b.length; ++i) {
            union[i][b.length] = -b[i];
        }
        union[b.length][b.length] = 1;
        return union;
    }

    private static double[] calculateSum(int j, double[][] a, double[][] v) {
        double[] res = new double[v.length];
        for (int i = 0; i < j; ++i) {
            res = plus(res, product(v[i], scalarProduct(a[j], v[i])));
        }
        return res;
    }

}
