<script>
    export let title = ""
    export let content = ""
    export let showCancelBtn = false
    export let closeBtnText = "Close"
    export let cancelBtnText = "Cancel"
    export let closeBtnCb = () => {}
    export let cancelBtnCb = () => {}
</script>

<div class="Modal">
    <div class="card-buffer">
        <div class="card">
            <h2>{title}</h2>
            <p>
                {content}
            </p>
            <div class="buttons">
                {#if showCancelBtn}
                <button on:click={cancelBtnCb}>{cancelBtnText}</button>
                {/if}
                <button on:click={closeBtnCb}>{closeBtnText}</button>
            </div>
        </div>
    </div>
    <div class="modal-bg" />
</div>

<style lang="scss">
    .Modal {
		position: absolute;
		height: 100%;
		width: 100%;
		top: 0;
		left: 0;
		.modal-bg {
			height: 100%;
			width: 100%;
			background-color: rgba(0, 0, 0, 0.5);
		}
		.card-buffer {
			position: absolute;
			height: 100%;
			width: 100%;
			display: flex;
			justify-content: center;
			align-items: center;
			.card {
				display: flex;
				flex-direction: column;
				text-align: left;
				gap: 10px;
				border-radius: 20px;
				position: absolute;
				display: flex;
				justify-content: center;
				width: 80%;
				background-color: #1a1a1a;
				color: white;
				padding: 20px;
			}

			@media (prefers-color-scheme: light) {
				.card {
					color: black;
					background-color: white;
				}
			}
		}
	}
</style>