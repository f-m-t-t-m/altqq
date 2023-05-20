import org.example.GaussLinearEquationSolver;
import org.example.GaussLinearEquationSolverColumnPivot;
import org.example.GaussLinearEquationSolverStrokePivot;
import org.example.MatrixUtils;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.Arrays;

import static org.junit.jupiter.api.Assertions.*;

public class GaussLinearEquationTest {

    double[][] a = {{2, 1, -1},
                    {-3, -1, 2},
                    {-2, 1, 2}};
    double[] b = {8, -11, -3};
    double[] expected = {2, 3, -1};

    @Test
    void test_forward_step() {
        new GaussLinearEquationSolver().forwardStep(a, b);
        assertTrue(MatrixUtils.isMatrixTriangular(a));
    }

    @Test
    void test_backward_step() {
        GaussLinearEquationSolver solver = new GaussLinearEquationSolver();
        solver.forwardStep(a, b);
        assertArrayEquals(solver.backwardStep(a, b), expected);
    }

}
