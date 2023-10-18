/*
 * elevator sstf
 */
#include <linux/blkdev.h>
#include <linux/elevator.h>
#include <linux/bio.h>
#include <linux/module.h>
#include <linux/slab.h>
#include <linux/init.h>
#include <linux/list_sort.h>

/* SSTF data structure. */
struct sstf_data {
	struct list_head queue;
	struct list_head *next_request;
	long long int last_blk_value;
};

static int sstf_compare(void *priv, struct list_head *a, struct list_head *b)
{
	struct request *req_a = list_entry(a, struct request, queuelist);
    struct request *req_b = list_entry(b, struct request, queuelist);
    struct sstf_data *sd = req_a->q->elevator->elevator_data;
    sector_t pos_a = blk_rq_pos(req_a);
    sector_t pos_b = blk_rq_pos(req_b);
    long long int diff_a = abs(pos_a - sd->last_blk_value);
    long long int diff_b = abs(pos_b - sd->last_blk_value);
	if (diff_a < diff_b) return -1;
    else if (diff_a > diff_b) return 1;
	else return 0;
}

static void sstf_merged_requests(struct request_queue *q, struct request *rq,
				 struct request *next)
{
	list_del_init(&next->queuelist);
}

static int sstf_dispatch(struct request_queue *q, int force)
{
	struct sstf_data *sd = q->elevator->elevator_data;
	char direction = 'R';
	struct request *rq;

	rq = list_first_entry_or_null(&sd->queue, struct request, queuelist);
	if (rq) {
		list_del_init(&rq->queuelist);
		elv_dispatch_sort(q, rq);
		sd->last_blk_value = blk_rq_pos(rq);
		printk(KERN_EMERG "[SSTF] dsp %c %llu\n", direction, blk_rq_pos(rq));

		return 1;
	}	
	return 0;
}

static void sstf_add_request(struct request_queue *q, struct request *rq)
{
    struct sstf_data *sd = q->elevator->elevator_data;
	char direction = 'R';

    list_add_tail(&rq->queuelist, &sd->queue);
	list_sort(NULL, &sd->queue, sstf_compare);
	printk(KERN_EMERG "[SSTF] add %c %llu\n", direction, blk_rq_pos(rq));
}

static int sstf_init_queue(struct request_queue *q, struct elevator_type *e){
	struct sstf_data *nd;
	struct elevator_queue *eq;

	/* Implementação da inicialização da fila (queue).
	 *
	 * Use como exemplo a inicialização da fila no driver noop-iosched.c
	 *
	 */

	eq = elevator_alloc(q, e);
	if (!eq)
		return -ENOMEM;

	nd = kmalloc_node(sizeof(*nd), GFP_KERNEL, q->node);
	if (!nd) {
		kobject_put(&eq->kobj);
		return -ENOMEM;
	}
	eq->elevator_data = nd;

	INIT_LIST_HEAD(&nd->queue);

	spin_lock_irq(q->queue_lock);
	q->elevator = eq;
	spin_unlock_irq(q->queue_lock);

	return 0;
}

static void sstf_exit_queue(struct elevator_queue *e)
{
	struct sstf_data *nd = e->elevator_data;

	/* Implementação da finalização da fila (queue).
	 *
	 * Use como exemplo o driver noop-iosched.c
	 *
	 */
	BUG_ON(!list_empty(&nd->queue));
	kfree(nd);
}

/* Infrastrutura dos drivers de IO Scheduling. */
static struct elevator_type elevator_sstf = {
	.ops.sq = {
		.elevator_merge_req_fn		= sstf_merged_requests,
		.elevator_dispatch_fn		= sstf_dispatch,
		.elevator_add_req_fn		= sstf_add_request,
		.elevator_init_fn		= sstf_init_queue,
		.elevator_exit_fn		= sstf_exit_queue,
	},
	.elevator_name = "sstf",
	.elevator_owner = THIS_MODULE,
};

static int __init sstf_init(void)
{
    return elv_register(&elevator_sstf);
}

static void __exit sstf_exit(void)
{
    elv_unregister(&elevator_sstf);
}

module_init(sstf_init);
module_exit(sstf_exit);

MODULE_AUTHOR("GiovaniGabrielLucas");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Shortest Seek Time First (SSTF) IO scheduler");
