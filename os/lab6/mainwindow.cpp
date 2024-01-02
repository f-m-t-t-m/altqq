#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>
#include <QJsonDocument>
#include <QJsonObject>
#include <QTimer>
#include <QJsonArray>
#include <QwtDateScaleDraw>
#include <QwtDateScaleEngine>
#include <QwtPlotCurve>
#include <QwtSymbol>
#include <QwtPlotGrid>

TempApi::TempApi(QObject* parent) : QObject(parent) { }

void TempApi::getCurrentTemperature() {
    QTextStream(stdout) << "getting current temperature from server" << Qt::endl;
    QNetworkRequest request(QUrl("http://127.0.0.1/current-temp"));
    QNetworkAccessManager* manager = new QNetworkAccessManager();
    QNetworkReply* reply = manager->get(request);
    QObject::connect(reply, &QNetworkReply::finished, [reply, this]() {
        QString ReplyText = reply->readAll();
        QJsonDocument doc = QJsonDocument::fromJson(ReplyText.toUtf8());
        QJsonObject obj = doc.object();
        QJsonValue value = obj.value(QString("currentTemp"));
        reply->deleteLater();
        double temp = value.toDouble();
        emit currentTemperatureSignal(temp);
    });
}

void TempApi::getDailyAvgTemperature(QDateTime start, QDateTime finish) {
    QTextStream(stdout) << "getting daily avg temperature from server" << Qt::endl;
    QString startStr = start.toString(QString("dd.MM.yyyy,%20hh:mm:ss"));
    QString finishStr = finish.toString(QString("dd.MM.yyyy,%20hh:mm:ss"));
    QUrl url = QUrl("http://127.0.0.1/temp-for-period/avg-hour?start=" + startStr + "&end="+finishStr);
    QNetworkRequest request(url);
    QNetworkAccessManager* manager = new QNetworkAccessManager();
    QNetworkReply* reply = manager->get(request);
    QObject::connect(reply, &QNetworkReply::finished, [reply, this]() {
        QString ReplyText = reply->readAll();
        QJsonDocument doc = QJsonDocument::fromJson(ReplyText.toUtf8());
        QJsonArray arr = doc.array();
        reply->deleteLater();
        emit dailyAvgTemperatureSignal(arr);
    });
}

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
    , m_tmr (new QTimer(this))
    , m_api(new TempApi(this)) {
    ui->setupUi(this);
    ui->dailyStartDateTime->setDisplayFormat(QString("dd.MM.yyyy hh:mm:ss"));
    ui->dailyStartDateTime->setDateTime(QDateTime::currentDateTime().addMonths(-1));
    ui->dailyEndDateTime->setDisplayFormat(QString("dd.MM.yyyy hh:mm:ss"));
    ui->dailyEndDateTime->setDateTime(QDateTime::currentDateTime());

    m_api->getDailyAvgTemperature(QDateTime::currentDateTime().addMonths(-1), QDateTime::currentDateTime());

    QwtDateScaleDraw* scaleDraw= new QwtDateScaleDraw(Qt::LocalTime);
    ui->qwtPlot->setAxisScaleDraw(QwtPlot::xBottom,scaleDraw);
    QwtDateScaleEngine * scaleEngine = new QwtDateScaleEngine( Qt::LocalTime );
    ui->qwtPlot->setAxisScaleEngine(QwtPlot::xBottom, scaleEngine);
    ui->qwtPlot->updateAxes();

    QwtPlotGrid *grid = new QwtPlotGrid();
    grid->attach(ui->qwtPlot);

    m_api->getCurrentTemperature();
    m_tmr->setInterval(1000);
    m_tmr->start();

    connect(ui->dailyStartDateTime, SIGNAL(dateTimeChanged(QDateTime)), this, SLOT(updateDailyPlotStartChange(QDateTime)));
    connect(ui->dailyEndDateTime, SIGNAL(dateTimeChanged(QDateTime)), this, SLOT(updateDailyPlotFinishChange(QDateTime)));
    connect(m_api,SIGNAL(currentTemperatureSignal(double)), this, SLOT(setCurrentTemperature(double)));
    connect(m_tmr,SIGNAL(timeout()), m_api,SLOT(getCurrentTemperature()));
    connect(m_api, SIGNAL(dailyAvgTemperatureSignal(QJsonArray)), this, SLOT(plotDailyAvgTemperature(QJsonArray)));
}

MainWindow::~MainWindow() {
    delete ui;
}

void MainWindow::updateDailyPlotStartChange(QDateTime start) {
    m_api->getDailyAvgTemperature(start, ui->dailyEndDateTime->dateTime());
}

void MainWindow::updateDailyPlotFinishChange(QDateTime finish) {
    m_api->getDailyAvgTemperature(ui->dailyStartDateTime->dateTime(), finish);
}

void MainWindow::setCurrentTemperature(double temp) {
    ui->currentTemp->display(temp);
}

void MainWindow::plotDailyAvgTemperature(QJsonArray arr) {
    QwtPlotCurve *curve = new QwtPlotCurve();
    curve->setPen( Qt::blue, 2 );
    curve->setRenderHint( QwtPlotItem::RenderAntialiased, true );
    QPolygonF points;
    for (const QJsonValue& v: arr) {
        points << QPointF(QwtDate::toDouble(QDateTime::fromString( v.toObject().value("date").toString(), "yyyy-MM-dd HH:mm:ss")),
                          v.toObject().value("temp").toDouble() );
    }
    curve->setSamples(points);
    QwtSymbol *symbol = new QwtSymbol( QwtSymbol::Ellipse,
                                      QBrush( Qt::yellow ), QPen( Qt::red, 2 ), QSize( 4, 4 ) );
    curve->setSymbol(symbol);
    curve->attach(ui->qwtPlot);
    ui->qwtPlot->replot();
}
