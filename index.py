from app import app, init_scheduler
# runs the app and the scheduler
if __name__ == '__main__':
	with app.app_context():
		init_scheduler()
		app.run(host="0.0.0.0", port=8080, debug=True,use_reloader=False)