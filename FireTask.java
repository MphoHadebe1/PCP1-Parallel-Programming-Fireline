import java.util.concurrent.RecursiveTask;

public class FireTask extends RecursiveTask<FireMapParallel.StepResult> {

    private final FireMapParallel map;
    private final FireMapParallel.Mode mode;
    private final int rowStart;
    private final int rowEnd;
    private final int columnStart;
    private final int columnEnd;
    private final int cutoff;

    public FireTask(FireMapParallel map,
                    FireMapParallel.Mode mode,
                    int rowStart,
                    int rowEnd,
                    int columnStart,
                    int columnEnd,
                    int cutoff) {
        this.map = map;
        this.mode = mode;
        this.rowStart = rowStart;
        this.rowEnd = rowEnd;
        this.columnStart = columnStart;
        this.columnEnd = columnEnd;
        this.cutoff = cutoff;
    }

    @Override
    protected FireMapParallel.StepResult compute() {
        int height = rowEnd - rowStart;
        int width = columnEnd - columnStart;

        if ((long) height * width <= cutoff || height < 2) {
            return map.updateRegion(
                    mode, rowStart, rowEnd, columnStart, columnEnd);
        }

        int middle = rowStart + height / 2;

        FireTask top = new FireTask(
                map, mode, rowStart, middle,
                columnStart, columnEnd, cutoff);
        FireTask bottom = new FireTask(
                map, mode, middle, rowEnd,
                columnStart, columnEnd, cutoff);

        top.fork();
        FireMapParallel.StepResult bottomResult = bottom.compute();
        FireMapParallel.StepResult topResult = top.join();

        return FireMapParallel.StepResult.combine(
                topResult, bottomResult);
    }
}
