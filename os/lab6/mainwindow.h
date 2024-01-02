#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QDateTime>
#include <QJsonArray>
#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui {
class MainWindow;
}
QT_END_NAMESPACE

class TempApi : public QObject {
    Q_OBJECT

public:
    TempApi(QObject* parent);
    virtual ~TempApi(){};
    void getDailyAvgTemperature(QDateTime, QDateTime);
public slots:
    void getCurrentTemperature();
signals:
    void currentTemperatureSignal(double);
    void dailyAvgTemperatureSignal(QJsonArray);
};

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
public slots:
    void setCurrentTemperature(double);
    void updateDailyPlotStartChange(QDateTime);
    void updateDailyPlotFinishChange(QDateTime);
    void plotDailyAvgTemperature(QJsonArray);

private:
    Ui::MainWindow *ui;
    QTimer*         m_tmr;
    TempApi*        m_api;
};
#endif // MAINWINDOW_H
