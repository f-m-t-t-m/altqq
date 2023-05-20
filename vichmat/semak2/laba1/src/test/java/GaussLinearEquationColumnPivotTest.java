import org.example.GaussLinearEquationSolverColumnPivot;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class GaussLinearEquationColumnPivotTest {

    double[][] a = {{2, 1, -1},
                    {-3, -1, 2},
                    {-2, 1, 2}};
    double[] b = {8, -11, -3};
    double[] expected = {2, 3, -1};

    @Test
    void test_get_column_pivot() {
        GaussLinearEquationSolverColumnPivot solver = new GaussLinearEquationSolverColumnPivot();
        assertEquals(1, solver.getColumnPivot(a, 0));
        assertEquals(1, solver.getColumnPivot(a, 1));
        assertEquals(2, solver.getColumnPivot(a, 2));
    }

    @Test
    void test_column_pivot() {
        GaussLinearEquationSolverColumnPivot solver = new GaussLinearEquationSolverColumnPivot();
        solver.forwardStep(a, b);
        double[] actual = solver.backwardStep(a, b);
        for (int i = 0; i < actual.length; ++i) {
            actual[i] = Math.round(actual[i] * 1e6) / 1e6;
        }
        assertArrayEquals(expected, actual);
    }


}
