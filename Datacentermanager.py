import multiprocessing
import time
import Dbaccessor

class Consumer(multiprocessing.Process):
    
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # task is completed
                print(proc_name + ': Exiting')
                self.task_queue.task_done()
                break
            print(proc_name + ' is running')
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)
        return


if __name__ == '__main__':
    # コミュニケーションキューを作成する
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    
    # consumers 処理を開始する
    num_consumers = multiprocessing.cpu_count() * 2
    print('Creating ' + str(num_consumers) + ' consumers')
    consumers = [ Consumer(tasks, results)
                  for i in range(num_consumers) ]

    for w in consumers:
        w.start()
    
    # ジョブをキューへ入れる
    num_jobs = 10
    for i in range(num_jobs):
        tasks.put([1, 123, 1000])
    
    # 各 consumer へ poison pill を追加する
    for i in range(num_consumers):
        tasks.put(None)




