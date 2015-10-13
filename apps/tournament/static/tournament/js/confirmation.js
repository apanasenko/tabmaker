function confirm_remove_round(href) {
    if (confirm('Удалить последний раунд? Все румы раунда и результаты будут удалены'))
        location.href = href;
}
