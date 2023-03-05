package cn.fefu;

public class Main {
    private static final double[][] A = {
            {2, -1, 0},
            {5, 4,  2},
            {0, 1,  -3}
    };

    private static final double[] B = {
            3, 6, 2
    };

    private static double[] solve(double[][] A, double[] B) {
        int len = B.length;
        double[] x = new double[len];
        double[] alpha = new double[len-1];
        double[] beta = new double[len-1];

        alpha[0] = -A[0][1] / A[0][0];
        beta[0] = B[0] / A[0][0];
        for(int i = 1; i < len - 1; ++i) {
            alpha[i] = -A[i][i+1] / (A[i][i] + A[i][i-1] * alpha[i-1]);
            beta[i] = (B[i] - A[i][i-1] * beta[i-1]) / (A[i][i] + A[i][i-1] * alpha[i-1]);
        }
        x[len-1] = (B[len-1] - A[len-1][len-2] * beta[len-2]) / (A[len-1][len-1] + A[len-1][len-2] * alpha[len-2]);

        for(int i = len - 1; i > 0; --i) {
            x[i-1] = x[i] * alpha[i-1] + beta[i-1];
        }

        for(int i = 0; i < len-1; ++i) {
            System.out.printf("alpha%d = %f ", i, alpha[i]);
        }
        System.out.println();
        for (int i = 0; i < len-1; ++i) {
            System.out.printf(" beta%d = %f ", i, beta[i]);
        }
        System.out.println();

        return x;
    }

    public static void main(String[] args) {
        double[] x = solve(A, B);
        for (int i = 0; i < x.length; ++i) {
            System.out.printf("    x%d = %f ", i, x[i]);
        }
    }

}