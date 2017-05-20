function confirm_remove_round(href) {
    if (confirm('Удалить последний раунд? Все результаты и комнаты раунда будут удалены'))
        location.href = href;
}
