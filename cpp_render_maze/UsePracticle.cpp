#include <bits/stdc++.h>
using namespace std;

int totalCell = 1;

struct Point
{
    int r;
    int c;
    int visited = false;

    Point()
    {
        this->r = 0;
        this->c = 0;
    }

    Point(int r, int c)
    {
        this->r = r;
        this->c = c;
    }
};

void PrintMaze(vector<vector<char>> maze, int rows, int cols)
{
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            cout << maze[i][j];
        }
        cout << endl;
    }
}

Point CheckNeighbours(vector<vector<char>> maze, Point current)
{
    // Nếu điểm hiện tại đang là điểm end thì sẽ xét kĩ hơn
    // Chỉ cần nó nằm trên viền thì có nghĩa là nó là điểm kết thúc
    if (current.r == 0 || current.r == maze.size() - 1 || current.c == 0 || current.c == maze[0].size() - 1)
    {
        // Chỉ có thể đi xuống
        if (current.r == 0)
        {
            return Point(1, current.c);
        }
        else if (current.r == maze.size() - 1)
        {
            return Point(maze.size() - 2, current.c);
        }
        else if (current.c == 0)
        {
            return Point(current.r, 1);
        }
        else if (current.c == maze.size() - 1)
        {
            return Point(current.r, maze.size() - 2);
        }
    }
    // Các điểm còn lại chỉ cần xét giới hạn viền xung quanh của nó
    vector<Point> allNeighbours;
    if (current.r > 1 && maze[current.r - 1][current.c] != ' ')
    {
        allNeighbours.push_back(Point(current.r - 1, current.c));
    }
    if (current.c < maze[0].size() - 2 && maze[current.r][current.c + 1] != ' ')
    {
        allNeighbours.push_back(Point(current.r, current.c + 1));
    }
    if (current.r < maze.size() - 2 && maze[current.r + 1][current.c] != ' ')
    {
        allNeighbours.push_back(Point(current.r + 1, current.c));
    }
    if (current.c > 1 && maze[current.r][current.c - 1] != ' ')
    {
        allNeighbours.push_back(Point(current.r, current.c - 1));
    }

    if (allNeighbours.size() != 0)
    {
        int random = rand() % allNeighbours.size();
        return allNeighbours[random];
    }
    else
    {
        return Point(0, 0);
    }
}

void GenerateBonus(vector<vector<char>>& maze, int bonus) {
    int nRows = maze.size();
    int nCols = maze[0].size();
    vector<int> rows;
    vector<int> cols;
    vector<int> vBonus;

    for (int i = 0; i < bonus; i++) {
        int r = rand() % nRows;
        int c = rand() % nCols;

        while (maze[r][c] != ' ') {
            r = rand() % nRows;
            c = rand() % nCols;
        }

        if (maze[r][c] == ' ') {
            maze[r][c] = '+';
            rows.push_back(r);
            cols.push_back(c);
            int temp = -(rand() % 50 + 1);
            vBonus.push_back(temp);
        }
    }

    cout << bonus << endl;
    for (int i = 0; i < bonus; i++) {
        cout << rows[i] << " " << cols[i] << " " << vBonus[i] << endl;
    }
    PrintMaze(maze, nRows, nCols);
}

int main()
{
    ios::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);
    srand(time(NULL));

    int rows, cols;
    // cin >> rows, cols;
    rows = 25;
    cols = 35;

    int bonus = 12;

    Point end;

    // Tìm một điểm là đầu ra của ma trận;
    int chooseOut = rand() % 4 + 1;

    int r, c;
    switch (chooseOut)
    {
        // Trường hợp điểm đầu ra nằm trên cạnh trên
    case 1:
        c = rand() % (cols - 1) + 1;
        end.r = 0;
        end.c = c;
        break;
        // Trường hợp điểm ra nằm ở trên cạnh phải
    case 2:
        r = rand() % (rows - 1) + 1;
        end.r = r;
        end.c = cols - 1;
        break;
        // Trường hợp điểm ra nằm ở cạnh dưới
    case 3:
        c = rand() % (cols - 1) + 1;
        end.r = rows - 1;
        end.c = c;
        break;
        // Trường hợp điểm ra nằm ở cạnh trái
    case 4:
        r = rand() % (rows - 1) + 1;
        end.r = r;
        end.c = 0;
        break;
    }

    vector<vector<char>> maze(rows);
    for (int i = 0; i < rows; i++)
    {
        maze[i].resize(cols, 'x');
    }

    maze[end.r][end.c] = 'E';

    // PrintMaze(maze, rows, cols);

    // Dùng DFS, duyệt từ điểm kết thúc duyệt ngược về
    // Duyệt đến khi nào số điểm duyệt được lớn hơn 70% số điểm đang có

    int allPoint = (rows - 2) * (cols - 2) * 0.7;
    int pointVisited = 1;

    stack<Point> listPoint;
    Point current = end;
    listPoint.push(end);
    while (listPoint.size() != 0 || pointVisited <= allPoint)
    {
        current.visited = true;

        Point next = CheckNeighbours(maze, current);

        if (next.r != 0)
        {
            next.visited = true;

            listPoint.push(next);

            maze[current.r][current.c] = ' ';

            current = next;
            pointVisited++;
        }
        else if (listPoint.size() != 0)
        {
            current = listPoint.top();
            listPoint.pop();
        }
    }

    Point start;
    r = rand() % (rows - 2) + 1;
    c = rand() % (cols - 2) + 1;

    while (maze[r][c] == ' ' && (pow((r - end.r), 2) + pow((c - end.c), 2)) * 2 < (pow((rows - 2), 2) + pow((cols - 2), 2)))
    {
        r = rand() % (rows - 2) + 1;
        c = rand() % (cols - 2) + 1;
    }

    maze[r][c] = '*';

    GenerateBonus(maze, bonus);
}
