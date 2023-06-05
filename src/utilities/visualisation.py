# ----------------------------------------------------------------------------
# Created By  : Sebastian Widmann
# Institution : TU Munich, Department of Aerospace and Geodesy
# Created Date: March 22, 2023
# version ='1.0'
# ---------------------------------------------------------------------------
from ml_collections import ConfigDict
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np


def plot_prediction(config: ConfigDict, predictions, ground_truth, epoch, name):
    fig, ax = plt.subplots(1, 2, figsize=(15, 5))

    xmin, xmax, ymin, ymax = config.preprocess.dim
    nx, ny = config.vit.img_size
    x, y = np.mgrid[xmin:xmax:(nx * 1j), ymin:ymax:(ny * 1j)]

    im0 = ax[0].pcolormesh(
        x, y, predictions,
        vmin=np.min(predictions),
        vmax=np.max(predictions)
    )

    im1 = ax[1].pcolormesh(
        x, y, ground_truth,
        vmin=np.min(ground_truth),
        vmax=np.max(ground_truth)
    )

    ax0_divider = make_axes_locatable(ax[0])
    ax1_divider = make_axes_locatable(ax[1])
    cax0 = ax0_divider.append_axes("right", "3%", pad="3%")
    cax1 = ax1_divider.append_axes("right", "3%", pad="3%")

    plt.colorbar(im0, cax=cax0, label='Predictions',
                 ticks=np.linspace(np.min(predictions), np.max(predictions),
                                   10, endpoint=True))

    plt.colorbar(im1, cax=cax1, label='Ground truth',
                 ticks=np.linspace(np.min(ground_truth), np.max(ground_truth),
                                   10, endpoint=True))

    # cax0.xaxis.set_ticks_position("top")
    # cax1.xaxis.set_ticks_position("top")

    plt.tight_layout()
    plt.subplots_adjust(hspace=2)

    # plt.show()
    if name == 0:
        field = 'p'
    elif name == 1:
        field = 'ux'
    elif name == 2:
        field = 'uy'
    plt.savefig('vit_{}_{}.png'.format(field, epoch), dpi=300)
    plt.close()


def plot_delta(config, predictions, ground_truth, epoch, cmap):
    fig, (ax, cax) = plt.subplots(ncols=3, nrows=2, figsize=(15, 6),
                                  gridspec_kw={"height_ratios": [1, 0.05]})

    xmin, xmax, ymin, ymax = config.preprocess.dim
    nx, ny = config.vit.img_size
    x, y = np.mgrid[xmin:xmax:(nx * 1j), ymin:ymax:(ny * 1j)]

    dp = ground_truth[:, :, 0] - predictions[:, :, 0]
    dux = ground_truth[:, :, 1] - predictions[:, :, 1]
    duy = ground_truth[:, :, 2] - predictions[:, :, 2]

    im0 = ax[0].pcolormesh(
        x, y, dp,
        cmap=cmap,
        vmin=np.min(dp),
        vmax=np.max(dp)
    )

    im1 = ax[1].pcolormesh(
        x, y, dux,
        cmap=cmap,
        vmin=np.min(dux),
        vmax=np.max(dux)
    )

    im2 = ax[2].pcolormesh(
        x, y, duy,
        cmap=cmap,
        vmin=np.min(duy),
        vmax=np.max(duy)
    )

    # Remove x and y coordinate ticks and labels

    # plt.setp(ax[0].get_xticklabels(), visible=False)
    # plt.setp(ax[0].get_yticklabels(), visible=False)
    # plt.setp(ax[1].get_xticklabels(), visible=False)
    # plt.setp(ax[1].get_yticklabels(), visible=False)
    # plt.setp(ax[2].get_xticklabels(), visible=False)
    # plt.setp(ax[2].get_yticklabels(), visible=False)
    # ax[0].tick_params(axis='both', which='both', length=0)
    # ax[1].tick_params(axis='both', which='both', length=0)
    # ax[2].tick_params(axis='both', which='both', length=0)

    plt.colorbar(im0, cax=cax[0], orientation='horizontal',
                 label='$\Delta p$ [-]',
                 ticks=np.linspace(np.min(dp), np.max(dp), 5, endpoint=True))

    plt.colorbar(im1, cax=cax[1], orientation='horizontal',
                 label='$\Delta u_x$ [-]',
                 ticks=np.linspace(np.min(dux), np.max(dux), 5, endpoint=True))

    plt.colorbar(im2, cax=cax[2], orientation='horizontal',
                 label='$\Delta u_y$ [-]',
                 ticks=np.linspace(np.min(duy), np.max(duy), 5, endpoint=True))

    plt.tight_layout()

    plt.savefig('vit_delta_{}.png'.format(epoch), dpi=300)
    plt.close()


def plot_loss(config: ConfigDict, train_loss, test_loss):
    fig, ax = plt.subplots(1, 1, figsize=(5, 5))

    x = range(0, config.num_epochs)

    ax.plot(x, train_loss, label='Train')
    ax.plot(x, test_loss, label='Test')

    ax.set_yscale('log')

    ax.set_xlim(0, config.num_epochs)
    ax.set_xlabel('Epochs')
    ax.set_ylabel('Mean Square Error')

    ax.legend(loc=1)

    plt.grid(visible=True, which='major', color='#444', linestyle='-')
    plt.grid(visible=True, which='minor', color='#ccc', linestyle='--')

    ax.set_title(
        'Epochs = {}, Batch size = {}, Lr = {}, Weight decay = {}'.format(
            config.num_epochs, config.batch_size,
            config.learning_rate_scheduler, config.weight_decay), fontsize=8)

    plt.tight_layout()

    plt.savefig('vit_loss.png', dpi=300)
    plt.close()
